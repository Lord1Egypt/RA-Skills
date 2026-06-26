#!/usr/bin/env tsx
/**
 * describe-table.ts - 查看表结构
 * 
 * 用法:
 *   tsx describe-table.ts --url "mysql://user:pass@host:port/db" --table users
 *   tsx describe-table.ts --db-type mysql --host localhost --port 3306 --user root --password secret --database mydb --table users
 * 
 * 输出格式: JSON { tableName, columns, indexes, primaryKey, foreignKeys }
 */

import { parseArgs } from 'node:util';

interface ConnectionConfig {
  dbType: 'mysql' | 'postgresql' | 'sqlite';
  host?: string;
  port?: number;
  user?: string;
  password?: string;
  database?: string;
}

interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  defaultValue: string | null;
  comment?: string;
}

interface TableSchema {
  tableName: string;
  columns: ColumnInfo[];
  primaryKey: string[];
  indexes: { name: string; columns: string[]; unique: boolean }[];
  foreignKeys: { name: string; columns: string[]; refTable: string; refColumns: string[] }[];
}

function parseConnectionUrl(url: string): ConnectionConfig {
  // SQLite 特殊处理：:memory: 和文件路径
  if (url.startsWith('sqlite://')) {
    const path = url.slice(9); // 去掉 'sqlite://'
    // 处理 :memory: 或文件路径
    const database = path === ':memory:' ? ':memory:' : decodeURIComponent(path);
    return { dbType: 'sqlite', database };
  }
  
  const parsed = new URL(url);
  const protocol = parsed.protocol.replace(':', '');
  
  const dbTypeMap: Record<string, 'mysql' | 'postgresql' | 'sqlite'> = {
    'mysql': 'mysql',
    'mysql2': 'mysql',
    'postgresql': 'postgresql',
    'postgres': 'postgresql',
    'pg': 'postgresql',
  };
  
  const dbType = dbTypeMap[protocol];
  if (!dbType) throw new Error(`Unsupported protocol: ${protocol}`);
  
  return {
    dbType,
    host: parsed.hostname,
    port: parsed.port ? parseInt(parsed.port) : undefined,
    user: parsed.username,
    password: parsed.password,
    database: parsed.pathname.slice(1),
  };
}

async function describeMySQLTable(config: ConnectionConfig, tableName: string): Promise<TableSchema> {
  // 使用 require 以支持 NODE_PATH 全局模块查找
  const mysql = require('mysql2/promise');
  
  const connection = await mysql.createConnection({
    host: config.host || 'localhost',
    port: config.port || 3306,
    user: config.user,
    password: config.password,
    database: config.database,
  });
  
  try {
    // 获取列信息
    const [columnRows] = await connection.query(
      `SELECT 
        COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT
       FROM information_schema.COLUMNS 
       WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
       ORDER BY ORDINAL_POSITION`,
      [config.database, tableName]
    );
    
    const columns: ColumnInfo[] = (columnRows as any[]).map(r => ({
      name: r.COLUMN_NAME,
      type: r.COLUMN_TYPE,
      nullable: r.IS_NULLABLE === 'YES',
      defaultValue: r.COLUMN_DEFAULT,
      comment: r.COLUMN_COMMENT || undefined,
    }));
    
    // 获取主键
    const [pkRows] = await connection.query(
      `SELECT COLUMN_NAME 
       FROM information_schema.KEY_COLUMN_USAGE 
       WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? AND CONSTRAINT_NAME = 'PRIMARY'
       ORDER BY ORDINAL_POSITION`,
      [config.database, tableName]
    );
    const primaryKey = (pkRows as any[]).map(r => r.COLUMN_NAME);
    
    // 获取索引
    const [idxRows] = await connection.query(
      `SELECT INDEX_NAME, COLUMN_NAME, NON_UNIQUE 
       FROM information_schema.STATISTICS 
       WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
       ORDER BY INDEX_NAME, SEQ_IN_INDEX`,
      [config.database, tableName]
    );
    
    const indexMap = new Map<string, { columns: string[]; unique: boolean }>();
    for (const r of idxRows as any[]) {
      if (!indexMap.has(r.INDEX_NAME)) {
        indexMap.set(r.INDEX_NAME, { columns: [], unique: !r.NON_UNIQUE });
      }
      indexMap.get(r.INDEX_NAME)!.columns.push(r.COLUMN_NAME);
    }
    const indexes = Array.from(indexMap.entries())
      .filter(([name]) => name !== 'PRIMARY')
      .map(([name, data]) => ({ name, ...data }));
    
    // 获取外键
    const [fkRows] = await connection.query(
      `SELECT 
        CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
       FROM information_schema.KEY_COLUMN_USAGE
       WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? AND REFERENCED_TABLE_NAME IS NOT NULL`,
      [config.database, tableName]
    );
    
    const fkMap = new Map<string, { columns: string[]; refTable: string; refColumns: string[] }>();
    for (const r of fkRows as any[]) {
      if (!fkMap.has(r.CONSTRAINT_NAME)) {
        fkMap.set(r.CONSTRAINT_NAME, { columns: [], refTable: r.REFERENCED_TABLE_NAME, refColumns: [] });
      }
      fkMap.get(r.CONSTRAINT_NAME)!.columns.push(r.COLUMN_NAME);
      fkMap.get(r.CONSTRAINT_NAME)!.refColumns.push(r.REFERENCED_COLUMN_NAME);
    }
    const foreignKeys = Array.from(fkMap.entries()).map(([name, data]) => ({ name, ...data }));
    
    return { tableName, columns, primaryKey, indexes, foreignKeys };
  } finally {
    await connection.end();
  }
}

async function describePostgreSQLTable(config: ConnectionConfig, tableName: string): Promise<TableSchema> {
  // 使用 require 以支持 NODE_PATH 全局模块查找
  const { Client } = require('pg');
  
  const client = new Client({
    host: config.host || 'localhost',
    port: config.port || 5432,
    user: config.user,
    password: config.password,
    database: config.database,
  });
  
  try {
    await client.connect();
    
    // 获取列信息
    const colResult = await client.query(
      `SELECT 
        column_name, data_type, is_nullable, column_default,
        character_maximum_length, numeric_precision, numeric_scale
       FROM information_schema.columns 
       WHERE table_schema = 'public' AND table_name = $1
       ORDER BY ordinal_position`,
      [tableName]
    );
    
    const columns: ColumnInfo[] = colResult.rows.map(r => {
      let type = r.data_type;
      if (r.character_maximum_length) {
        type += `(${r.character_maximum_length})`;
      } else if (r.numeric_precision) {
        type += `(${r.numeric_precision}${r.numeric_scale ? ',' + r.numeric_scale : ''})`;
      }
      return {
        name: r.column_name,
        type,
        nullable: r.is_nullable === 'YES',
        defaultValue: r.column_default,
      };
    });
    
    // 获取主键
    const pkResult = await client.query(
      `SELECT a.attname
       FROM pg_index i
       JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
       WHERE i.indrelid = $1::regclass AND i.indisprimary`,
      [tableName]
    );
    const primaryKey = pkResult.rows.map(r => r.attname);
    
    // 获取索引
    const idxResult = await client.query(
      `SELECT 
        i.relname as index_name,
        array_agg(a.attname ORDER BY array_position(ix.indkey, a.attnum)) as columns,
        NOT ix.indisunique as is_non_unique
       FROM pg_index ix
       JOIN pg_class t ON t.oid = ix.indrelid
       JOIN pg_class i ON i.oid = ix.indexrelid
       JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
       WHERE t.relname = $1 AND NOT ix.indisprimary
       GROUP BY i.relname, ix.indisunique`,
      [tableName]
    );
    const indexes = idxResult.rows.map(r => ({
      name: r.index_name,
      columns: r.columns,
      unique: !r.is_non_unique,
    }));
    
    // 获取外键
    const fkResult = await client.query(
      `SELECT
        tc.constraint_name,
        kcu.column_name,
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
       FROM information_schema.table_constraints AS tc
       JOIN information_schema.key_column_usage AS kcu
         ON tc.constraint_name = kcu.constraint_name
       JOIN information_schema.constraint_column_usage AS ccu
         ON ccu.constraint_name = tc.constraint_name
       WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = $1`,
      [tableName]
    );
    
    const fkMap = new Map<string, { columns: string[]; refTable: string; refColumns: string[] }>();
    for (const r of fkResult.rows) {
      if (!fkMap.has(r.constraint_name)) {
        fkMap.set(r.constraint_name, { columns: [], refTable: r.foreign_table_name, refColumns: [] });
      }
      fkMap.get(r.constraint_name)!.columns.push(r.column_name);
      fkMap.get(r.constraint_name)!.refColumns.push(r.foreign_column_name);
    }
    const foreignKeys = Array.from(fkMap.entries()).map(([name, data]) => ({ name, ...data }));
    
    return { tableName, columns, primaryKey, indexes, foreignKeys };
  } finally {
    await client.end();
  }
}

async function describeSQLiteTable(config: ConnectionConfig, tableName: string): Promise<TableSchema> {
  // 使用 require 以支持 NODE_PATH 全局模块查找
  const Database = require('better-sqlite3');
  const db = new Database(config.database!);
  
  try {
    // 获取表结构
    const tableInfo = db.prepare(`PRAGMA table_info(${tableName})`).all() as any[];
    const columns: ColumnInfo[] = tableInfo.map(r => ({
      name: r.name,
      type: r.type,
      nullable: !r.notnull,
      defaultValue: r.dflt_value,
    }));
    
    // 主键
    const primaryKey = tableInfo.filter(r => r.pk > 0).sort((a, b) => a.pk - b.pk).map(r => r.name);
    
    // 索引
    const indexList = db.prepare(`PRAGMA index_list(${tableName})`).all() as any[];
    const indexes: { name: string; columns: string[]; unique: boolean }[] = [];
    
    for (const idx of indexList) {
      if (idx.origin === 'pk') continue; // 跳过主键索引
      const indexInfo = db.prepare(`PRAGMA index_info(${idx.name})`).all() as any[];
      indexes.push({
        name: idx.name,
        columns: indexInfo.map(i => i.name),
        unique: idx.unique === 1,
      });
    }
    
    // 外键
    const fkList = db.prepare(`PRAGMA foreign_key_list(${tableName})`).all() as any[];
    const fkMap = new Map<string, { columns: string[]; refTable: string; refColumns: string[] }>();
    
    for (const fk of fkList) {
      const key = `fk_${fk.id}`;
      if (!fkMap.has(key)) {
        fkMap.set(key, { columns: [], refTable: fk.table, refColumns: [] });
      }
      fkMap.get(key)!.columns.push(fk.from);
      fkMap.get(key)!.refColumns.push(fk.to);
    }
    const foreignKeys = Array.from(fkMap.entries()).map(([name, data]) => ({ name, ...data }));
    
    return { tableName, columns, primaryKey, indexes, foreignKeys };
  } finally {
    db.close();
  }
}

async function main() {
  const { values } = parseArgs({
    options: {
      'db-type': { type: 'string', short: 't' },
      'host': { type: 'string', short: 'h' },
      'port': { type: 'string', short: 'P' },
      'user': { type: 'string', short: 'u' },
      'password': { type: 'string', short: 'p' },
      'database': { type: 'string', short: 'd' },
      'url': { type: 'string' },
      'table': { type: 'string', short: 'T' },
    },
    strict: false,
  });
  
  const tableName = values.table as string;
  if (!tableName) {
    console.error('Error: --table is required');
    process.exit(1);
  }
  
  let config: ConnectionConfig;
  
  if (values.url) {
    config = parseConnectionUrl(values.url as string);
  } else {
    config = {
      dbType: values['db-type'] as 'mysql' | 'postgresql' | 'sqlite',
      host: values.host as string,
      port: values.port ? parseInt(values.port as string) : undefined,
      user: values.user as string,
      password: values.password as string,
      database: values.database as string,
    };
  }
  
  if (!config.dbType) {
    console.error('Error: --db-type or --url is required');
    process.exit(1);
  }
  
  let schema: TableSchema;
  
  switch (config.dbType) {
    case 'mysql':
      schema = await describeMySQLTable(config, tableName);
      break;
    case 'postgresql':
      schema = await describePostgreSQLTable(config, tableName);
      break;
    case 'sqlite':
      schema = await describeSQLiteTable(config, tableName);
      break;
    default:
      throw new Error(`Unsupported database type: ${config.dbType}`);
  }
  
  console.log(JSON.stringify(schema, null, 2));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});

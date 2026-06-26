#!/usr/bin/env tsx
/**
 * list-tables.ts - 列出数据库中的所有表
 * 
 * 用法:
 *   tsx list-tables.ts --url "mysql://user:pass@host:port/db"
 *   tsx list-tables.ts --db-type mysql --host localhost --port 3306 --user root --password secret --database mydb
 * 
 * 输出格式: JSON { tables: string[], count: number }
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

async function listMySQLTables(config: ConnectionConfig): Promise<string[]> {
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
    const [rows] = await connection.query(
      'SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = "BASE TABLE" ORDER BY TABLE_NAME',
      [config.database]
    );
    return (rows as any[]).map(r => r.TABLE_NAME);
  } finally {
    await connection.end();
  }
}

async function listPostgreSQLTables(config: ConnectionConfig): Promise<string[]> {
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
    const result = await client.query(
      "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name"
    );
    return result.rows.map(r => r.table_name);
  } finally {
    await client.end();
  }
}

async function listSQLiteTables(config: ConnectionConfig): Promise<string[]> {
  // 使用 require 以支持 NODE_PATH 全局模块查找
  const Database = require('better-sqlite3');
  const db = new Database(config.database!);
  
  try {
    const rows = db.prepare(
      "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).all() as { name: string }[];
    return rows.map(r => r.name);
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
    },
    strict: false,
  });
  
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
    console.error('Supported types: mysql, postgresql, sqlite');
    process.exit(1);
  }
  
  let tables: string[];
  
  switch (config.dbType) {
    case 'mysql':
      tables = await listMySQLTables(config);
      break;
    case 'postgresql':
      tables = await listPostgreSQLTables(config);
      break;
    case 'sqlite':
      tables = await listSQLiteTables(config);
      break;
    default:
      throw new Error(`Unsupported database type: ${config.dbType}`);
  }
  
  console.log(JSON.stringify({ tables, count: tables.length }, null, 2));
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});

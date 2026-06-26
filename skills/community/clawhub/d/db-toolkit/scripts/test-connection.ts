#!/usr/bin/env tsx
/**
 * test-connection.ts - 测试数据库连接
 * 
 * 用法:
 *   tsx test-connection.ts --url "mysql://user:pass@host:port/db"
 *   tsx test-connection.ts --db-type mysql --host localhost --port 3306 --user root --password secret --database mydb
 */

import { parseArgs } from 'node:util';

interface ConnectionConfig {
  dbType: 'mysql' | 'postgresql' | 'sqlite';
  host?: string;
  port?: number;
  user?: string;
  password?: string;
  database?: string;
  url?: string;
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
  if (!dbType) {
    throw new Error(`Unsupported database protocol: ${protocol}`);
  }
  
  return {
    dbType,
    host: parsed.hostname,
    port: parsed.port ? parseInt(parsed.port) : undefined,
    user: parsed.username,
    password: parsed.password,
    database: parsed.pathname.slice(1),
  };
}

async function testMySQLConnection(config: ConnectionConfig): Promise<{ success: boolean; message: string; version?: string }> {
  try {
    // 使用 require 以支持 NODE_PATH 全局模块查找
    const { createConnection } = require('mysql2/promise');
    const connection = await createConnection({
      host: config.host,
      port: config.port || 3306,
      user: config.user,
      password: config.password,
      database: config.database,
      connectTimeout: 10000,
    });
    
    const [rows] = await connection.execute('SELECT VERSION() as version');
    const version = (rows as any[])[0]?.version;
    await connection.end();
    
    return { success: true, message: 'MySQL 连接成功', version };
  } catch (error: any) {
    return { success: false, message: `MySQL 连接失败: ${error.message}` };
  }
}

async function testPostgreSQLConnection(config: ConnectionConfig): Promise<{ success: boolean; message: string; version?: string }> {
  try {
    // 使用 require 以支持 NODE_PATH 全局模块查找
    const { Client } = require('pg');
    const client = new Client({
      host: config.host,
      port: config.port || 5432,
      user: config.user,
      password: config.password,
      database: config.database,
      connectionTimeoutMillis: 10000,
    });
    
    await client.connect();
    const result = await client.query('SELECT version()');
    const version = result.rows[0]?.version?.split(',')[0];
    await client.end();
    
    return { success: true, message: 'PostgreSQL 连接成功', version };
  } catch (error: any) {
    return { success: false, message: `PostgreSQL 连接失败: ${error.message}` };
  }
}

async function testSQLiteConnection(config: ConnectionConfig): Promise<{ success: boolean; message: string; version?: string }> {
  try {
    // 使用 require 以支持 NODE_PATH 全局模块查找
    const Database = require('better-sqlite3');
    const db = new Database(config.database as string);
    
    const result = db.prepare('SELECT sqlite_version() as version').get() as { version: string };
    db.close();
    
    return { success: true, message: 'SQLite 连接成功', version: `SQLite ${result.version}` };
  } catch (error: any) {
    return { success: false, message: `SQLite 连接失败: ${error.message}` };
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
    const dbType = (values['db-type'] as string)?.toLowerCase();
    if (!['mysql', 'postgresql', 'sqlite'].includes(dbType)) {
      console.error('错误: 必须指定 --db-type (mysql/postgresql/sqlite) 或 --url');
      process.exit(1);
    }
    config = {
      dbType: dbType as 'mysql' | 'postgresql' | 'sqlite',
      host: values.host as string,
      port: values.port ? parseInt(values.port as string) : undefined,
      user: values.user as string,
      password: values.password as string,
      database: values.database as string,
    };
  }

  console.log(`\n测试 ${config.dbType.toUpperCase()} 连接...`);
  console.log('─'.repeat(50));

  let result: { success: boolean; message: string; version?: string };
  
  switch (config.dbType) {
    case 'mysql':
      result = await testMySQLConnection(config);
      break;
    case 'postgresql':
      result = await testPostgreSQLConnection(config);
      break;
    case 'sqlite':
      result = await testSQLiteConnection(config);
      break;
    default:
      throw new Error(`Unsupported database type: ${config.dbType}`);
  }

  console.log(`状态: ${result.success ? '✅ 成功' : '❌ 失败'}`);
  console.log(`消息: ${result.message}`);
  if (result.version) {
    console.log(`版本: ${result.version}`);
  }
  console.log('─'.repeat(50));
  
  process.exit(result.success ? 0 : 1);
}

main().catch((error) => {
  console.error('执行出错:', error.message);
  process.exit(1);
});

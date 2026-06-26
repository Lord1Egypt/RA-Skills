/**
 * ClawMem 数据库初始化
 * 创建三层存储结构：L0 索引 / L1 时间线 / L2 详情
 */

import Database from 'better-sqlite3';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import config from '../config/loader.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const dbPath = join(__dirname, '..', config.database.path);
const db = new Database(dbPath);

// 启用 WAL 模式（更好的并发性能）
if (config.database.walMode) {
  db.pragma('journal_mode = WAL');
  console.log('✅ 数据库 WAL 模式已启用');
}

// L0: 极简索引目录（每条记录 < 100 bytes）
db.exec(`
  CREATE TABLE IF NOT EXISTS l0_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,           -- 分类：session/query/tool/memory
    timestamp INTEGER NOT NULL,        -- Unix 时间戳
    summary TEXT NOT NULL,             -- 极简摘要 (< 100 chars)
    token_cost INTEGER DEFAULT 0,      -- Token 消耗估算
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
  )
`);

// L1: 时间线（中等密度，按时间排序）
db.exec(`
  CREATE TABLE IF NOT EXISTS l1_timeline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT UNIQUE NOT NULL,
    session_id TEXT,                   -- 会话 ID
    event_type TEXT NOT NULL,          -- 事件类型
    timestamp INTEGER NOT NULL,
    semantic_summary TEXT,             -- 语义摘要 (< 500 chars)
    tags TEXT,                         -- 标签 JSON 数组
    token_cost INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
  )
`);

// L2: 完整详情（按需加载）
db.exec(`
  CREATE TABLE IF NOT EXISTS l2_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT UNIQUE NOT NULL,
    full_content TEXT,                 -- 完整内容
    metadata TEXT,                     -- 元数据 JSON
    embeddings TEXT,                   -- 向量嵌入（未来扩展）
    token_cost INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
  )
`);

// 生命周期事件表
db.exec(`
  CREATE TABLE IF NOT EXISTS lifecycle_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,          -- 事件名称
    session_id TEXT,
    timestamp INTEGER NOT NULL,
    processed INTEGER DEFAULT 0,       -- 是否已处理
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
  )
`);

// 创建索引（加速查询）
db.exec(`
  CREATE INDEX IF NOT EXISTS idx_l0_category ON l0_index(category);
  CREATE INDEX IF NOT EXISTS idx_l0_timestamp ON l0_index(timestamp);
  CREATE INDEX IF NOT EXISTS idx_l1_session ON l1_timeline(session_id);
  CREATE INDEX IF NOT EXISTS idx_l1_timestamp ON l1_timeline(timestamp);
  CREATE INDEX IF NOT EXISTS idx_l2_record ON l2_details(record_id);
  CREATE INDEX IF NOT EXISTS idx_lifecycle_event ON lifecycle_events(event_name);
`);

console.log('✅ ClawMem 数据库初始化完成');
console.log(`📍 数据库位置：${join(__dirname, '..', 'clawmem.db')}`);

export default db;

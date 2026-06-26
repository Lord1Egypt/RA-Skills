#!/usr/bin/env node
/**
 * 对话捕获器 - 扫描会话文件，捕获用户和 AI 消息
 * 
 * 用法：
 *   node conversation_capture.cjs           # 单次扫描
 *   node conversation_capture.cjs --daemon  # 守护进程模式
 */

const fs = require('fs');
const path = require('path');

// 确定技能目录
const SKILL_DIR = process.env.COGNITIVE_BRAIN_DIR || 
                  path.resolve(__dirname, '..', '..');

// 加载 pg 模块（使用绝对路径）
const { Pool } = require(path.join(SKILL_DIR, 'node_modules', 'pg'));

// 配置
const SESSIONS_DIR = '/root/.openclaw/agents/main/sessions';
const PROCESSED_MARKER = path.join(SESSIONS_DIR, '.conversation-processed.json');
const DAEMON_INTERVAL = 30000; // 30 秒

// 数据库配置
const dbConfig = {
  host: 'localhost',
  port: 5432,
  database: 'cognitive_brain',
  user: 'postgres',
  password: 'postgres'
};

let pool = null;

function getPool() {
  if (!pool) {
    pool = new Pool(dbConfig);
  }
  return pool;
}

// 记录已处理的位置 { sessionId: fileSize }
let processedPositions = {};

function loadProcessedPositions() {
  try {
    if (fs.existsSync(PROCESSED_MARKER)) {
      processedPositions = JSON.parse(fs.readFileSync(PROCESSED_MARKER, 'utf8'));
      console.log('[Capture] Loaded positions for', Object.keys(processedPositions).length, 'sessions');
    }
  } catch (e) {
    console.error('[Capture] Failed to load positions:', e.message);
  }
}

function saveProcessedPositions() {
  try {
    fs.writeFileSync(PROCESSED_MARKER, JSON.stringify(processedPositions, null, 2));
  } catch (e) {
    console.error('[Capture] Failed to save positions:', e.message);
  }
}

// 提取消息内容
function extractContent(msg) {
  if (!msg.message) return null;
  
  const role = msg.message.role;
  let content = null;
  
  if (typeof msg.message.content === 'string') {
    content = msg.message.content;
  } else if (Array.isArray(msg.message.content)) {
    content = msg.message.content
      .map(c => c.text || '')
      .join('\n');
  }
  
  return { role, content };
}

// 提取频道信息
function extractChannel(content) {
  // 从 metadata 中提取
  const match = content?.match(/"channel":\s*"([^"]+)"/);
  return match ? match[1] : 'unknown';
}

// 编码消息到数据库
async function encodeMessage(content, role, channel, timestamp) {
  const pg = getPool();
  
  try {
    // 检查是否已存在（基于内容哈希去重）
    const contentHash = Buffer.from(content).toString('base64').slice(0, 50);
    const existing = await pg.query(
      'SELECT id FROM episodes WHERE content = $1 AND role = $2 LIMIT 1',
      [content.slice(0, 2000), role]  // 截断以避免超长内容
    );
    
    if (existing.rows.length > 0) {
      return { status: 'duplicate', id: existing.rows[0].id };
    }
    
    // 插入新记录
    const result = await pg.query(`
      INSERT INTO episodes (content, summary, type, role, source_channel, importance, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING id
    `, [
      content.slice(0, 2000),  // 限制长度
      content.slice(0, 200),   // 摘要
      'episodic',
      role,
      channel || 'unknown',
      role === 'user' ? 0.7 : 0.5,  // 用户消息重要性更高
      timestamp ? new Date(timestamp) : new Date()
    ]);
    
    return { status: 'created', id: result.rows[0].id };
  } catch (err) {
    console.error('[Capture] Encode error:', err.message);
    return { status: 'error', error: err.message };
  }
}

// 扫描单个会话文件
async function scanSessionFile(filename) {
  const filepath = path.join(SESSIONS_DIR, filename);
  const sessionId = filename.replace('.jsonl', '');
  
  // 跳过非会话文件
  if (filename.includes('.reset.') || filename.includes('.lock')) {
    return { captured: 0, skipped: true };
  }
  
  try {
    const stats = fs.statSync(filepath);
    const lastSize = processedPositions[sessionId] || 0;
    
    // 文件没有增长，跳过
    if (stats.size <= lastSize) {
      return { captured: 0, noChange: true };
    }
    
    // 读取新增内容
    const fd = fs.openSync(filepath, 'r');
    const buffer = Buffer.alloc(stats.size - lastSize);
    fs.readSync(fd, buffer, 0, buffer.length, lastSize);
    fs.closeSync(fd);
    
    const newContent = buffer.toString('utf8');
    const lines = newContent.split('\n').filter(l => l.trim());
    
    const results = {
      user: 0,
      assistant: 0,
      errors: 0
    };
    
    for (const line of lines) {
      try {
        const msg = JSON.parse(line);
        
        // 只处理消息类型
        if (msg.type !== 'message') continue;
        
        const extracted = extractContent(msg);
        if (!extracted || !extracted.content) continue;
        
        const { role, content } = extracted;
        
        // 只捕获 user 和 assistant，跳过 toolResult
        if (role !== 'user' && role !== 'assistant') continue;
        
        // 跳过太短的内容（可能是系统消息）
        if (content.length < 10) continue;
        
        // 跳过 cron 任务消息（会污染记忆）
        if (content.includes('[cron:') && content.includes('Current time:')) {
          continue;
        }
        
        // 提取频道
        const channel = extractChannel(content);
        
        // 编码到数据库
        const result = await encodeMessage(
          content,
          role,
          channel,
          msg.timestamp
        );
        
        if (result.status === 'created') {
          results[role]++;
          console.log(`[Capture] ${role}: ${result.id} (${content.slice(0, 50)}...)`);
        }
      } catch (e) {
        results.errors++;
      }
    }
    
    // 更新处理位置
    processedPositions[sessionId] = stats.size;
    
    return {
      captured: results.user + results.assistant,
      user: results.user,
      assistant: results.assistant,
      errors: results.errors
    };
    
  } catch (err) {
    console.error('[Capture] Scan error:', err.message);
    return { captured: 0, error: err.message };
  }
}

// 单次扫描
async function runOnce() {
  console.log('[Capture] Starting single scan...');
  
  loadProcessedPositions();
  
  const files = fs.readdirSync(SESSIONS_DIR)
    .filter(f => f.endsWith('.jsonl') && !f.includes('.reset.'));
  
  console.log('[Capture] Found', files.length, 'session files');
  
  let total = { captured: 0, user: 0, assistant: 0 };
  
  for (const file of files) {
    const result = await scanSessionFile(file);
    total.captured += result.captured;
    total.user += result.user || 0;
    total.assistant += result.assistant || 0;
  }
  
  saveProcessedPositions();
  
  console.log(`[Capture] Done. Captured: ${total.captured} (user: ${total.user}, assistant: ${total.assistant})`);
  
  // 关闭数据库连接
  if (pool) await pool.end();
}

// 守护进程模式
async function runDaemon() {
  console.log('[Capture] Starting daemon mode...');
  console.log('[Capture] Interval:', DAEMON_INTERVAL, 'ms');
  
  loadProcessedPositions();
  
  while (true) {
    try {
      const files = fs.readdirSync(SESSIONS_DIR)
        .filter(f => f.endsWith('.jsonl') && !f.includes('.reset.'));
      
      let total = 0;
      
      for (const file of files) {
        const result = await scanSessionFile(file);
        total += result.captured;
      }
      
      if (total > 0) {
        console.log(`[Capture] Captured ${total} messages this round`);
        saveProcessedPositions();
      }
      
    } catch (err) {
      console.error('[Capture] Daemon error:', err.message);
    }
    
    await new Promise(resolve => setTimeout(resolve, DAEMON_INTERVAL));
  }
}

// 主入口
const args = process.argv.slice(2);
const isDaemon = args.includes('--daemon');

if (isDaemon) {
  runDaemon().catch(err => {
    console.error('[Capture] Fatal error:', err);
    process.exit(1);
  });
} else {
  runOnce().catch(err => {
    console.error('[Capture] Fatal error:', err);
    process.exit(1);
  });
}

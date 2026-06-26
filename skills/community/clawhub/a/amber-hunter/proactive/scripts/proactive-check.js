#!/usr/bin/env node
/**
 * amber-proactive V4: Fully self-contained extraction
 * 
 * 三步全部在脚本内完成，cron 直接触发，不需要 agent 介入。
 * 
 * 触发方式：
 * - 自动: cron 每15分钟运行此脚本 → 检查阈值 → LLM提取 → 写胶囊
 * - 手动: agent 调用此脚本（任何对话量都触发）
 * 
 * 触发阈值：
 * - 自动模式: session 消息数 ≥ 20 条
 * - 手动模式: 无限制（任意对话量）
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const http = require('http');

const HOME = os.homedir();
const SESSIONS_DIR = path.join(HOME, '.openclaw', 'agents', 'main', 'sessions');
const PENDING_FILE = path.join(HOME, '.amber-hunter', 'pending_extract.jsonl');
const CONFIG_PATH   = path.join(HOME, '.amber-hunter', 'config.json');
const OPENCLAW_CONFIG = path.join(HOME, '.openclaw', 'openclaw.json');
const LOG_PATH = path.join(HOME, '.amber-hunter', 'amber-proactive.log');

const AMBER_PORT = 18998;
const MIN_MESSAGES_THRESHOLD = 20;

// ── Logging ────────────────────────────────────────────────────────────

function log(msg) {
  const ts = new Date().toISOString().slice(11, 19);
  fs.appendFileSync(LOG_PATH, `[${ts}] ${msg}\n`);
  console.log(`[${ts}] ${msg}`);
}

// ── Config ────────────────────────────────────────────────────────────

function getConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch { return {}; }
}

function getApiKey() {
  // Read from OpenClaw config: models.providers['minimax-cn'].apiKey
  try {
    const openclawConfig = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG, 'utf8'));
    return openclawConfig?.models?.providers?.['minimax-cn']?.apiKey || '';
  } catch { return ''; }
}

// ── v1.2.8: Amber /extract endpoint (Proactive V4) ───────────────────

/**
 * Call amber-hunter's /extract endpoint to get structured memories.
 * Falls back to writing pending_extract.jsonl on failure (compat).
 */
function callExtractEndpoint(conversation, sessionId, amberToken) {
  return new Promise((resolve) => {
    const bodyObj = { text: conversation, source: sessionId };
    const bodyStr = JSON.stringify(bodyObj);
    const opts = {
      hostname: 'localhost',
      port: AMBER_PORT,
      path: '/extract',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${amberToken}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    };
    const req = http.request(opts, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          log(`[extract] HTTP ${res.statusCode}, falling back to pending file`);
          // Fallback: write pending_extract.jsonl for later processing
          try {
            fs.mkdirSync(path.dirname(PENDING_FILE), { recursive: true });
            fs.appendFileSync(PENDING_FILE, JSON.stringify({
              session_id: sessionId,
              text: conversation.slice(0, 4000),
              message_count: (conversation.match(/\n/g) || []).length,
              queued_at: new Date().toISOString(),
            }) + '\n');
          } catch (e2) { /* ignore */ }
          resolve([]);
          return;
        }
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.memories || []);
        } catch (e) {
          log(`[extract] Parse error: ${e.message}, raw: ${data.slice(0, 100)}`);
          resolve([]);
        }
      });
    });
    req.on('error', e => {
      log(`[extract] Connection error: ${e.message}, falling back to pending file`);
      try {
        fs.mkdirSync(path.dirname(PENDING_FILE), { recursive: true });
        fs.appendFileSync(PENDING_FILE, JSON.stringify({
          session_id: sessionId,
          text: conversation.slice(0, 4000),
          message_count: (conversation.match(/\n/g) || []).length,
          queued_at: new Date().toISOString(),
        }) + '\n');
      } catch (e2) { /* ignore */ }
      resolve([]);
    });
    req.write(bodyStr);
    req.end();
  });
}

// ── Session Reading ────────────────────────────────────────────────────

function getLatestSession() {
  try {
    const files = fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.endsWith('.jsonl'))
      .map(f => ({
        name: f,
        mtime: fs.statSync(path.join(SESSIONS_DIR, f)).mtime.getTime()
      }))
      .sort((a, b) => b.mtime - a.mtime);
    return files[0] ? path.join(SESSIONS_DIR, files[0].name) : null;
  } catch { return null; }
}

function extractMessages(sessionPath) {
  try {
    const content = fs.readFileSync(sessionPath, 'utf8');
    const lines = content.split('\n').filter(l => l.trim());
    const messages = [];
    for (const line of lines) {
      let d;
      try { d = JSON.parse(line); } catch { continue; }
      if (d.type !== 'message') continue;
      const raw = d.message;
      if (!raw || typeof raw !== 'object') continue;
      const parts = raw.content || [];
      let text = '';
      if (Array.isArray(parts)) {
        text = parts.map(p =>
          typeof p === 'string' ? p : (p && p.type === 'text' ? p.text : '')
        ).join('\n');
      } else if (typeof parts === 'string') {
        text = parts;
      }
      text = text.trim();
      if (!text || text.length < 10) continue;
      // 过滤掉日志行（时间戳格式 [HH:MM:SS] 或 ❌ 开头）
      if (/^\[\d{2}:\d{2}:\d{2}\]/.test(text) || text.startsWith('❌')) continue;
      messages.push({ role: raw.role || '?', text });
    }
    return messages;
  } catch { return []; }
}

function buildConversationText(messages, maxChars = 8000) {
  const recent = messages.slice(-50);
  const text = recent.map(m => `[${m.role}]: ${m.text}`).join('\n');
  return text.length > maxChars ? text.slice(-maxChars) : text;
}

// ── Amber API ────────────────────────────────────────────────────────

function getAmberToken() {
  return new Promise(resolve => {
    http.get({ hostname: 'localhost', port: AMBER_PORT, path: '/token' }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try { resolve(JSON.parse(data).api_key); } catch { resolve(''); }
      });
    }).on('error', () => resolve(''));
  });
}

function writeCapsule(token, memo, content, tags) {
  return new Promise(resolve => {
    // memo 最多80字符，整句不断词
    const memoText = memo.length > 80 ? memo.slice(0, 77) + '…' : memo;
    const capsule = { memo: memoText, content, tags };
    const bodyStr = JSON.stringify(capsule);
    const opts = {
      hostname: 'localhost', port: AMBER_PORT, path: '/capsules',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    };
    const req = http.request(opts, res => {
      res.resume();
      resolve(res.statusCode === 200 || res.statusCode === 201);
    });
    req.on('error', () => resolve(false));
    req.write(bodyStr);
    req.end();
  });
}

// ── Main ─────────────────────────────────────────────────────────────

async function main() {
  const isManual = process.argv.includes('--manual');

  // v1.2.8: Get amber-hunter token first (needed for /extract endpoint)
  const amberToken = await getAmberToken();
  if (!amberToken) {
    log('[main] No amber-hunter token found, skipping');
    return;
  }

  const sessionPath = getLatestSession();
  if (!sessionPath) {
    log('[main] No session file found');
    return;
  }

  const sessionId = path.basename(sessionPath, '.jsonl');
  const messages = extractMessages(sessionPath);

  log(`[main] Session ${sessionId}: ${messages.length} messages`);

  // 检查阈值
  if (!isManual && messages.length < MIN_MESSAGES_THRESHOLD) {
    log(`[main] Skipping: ${messages.length} messages (need ≥ ${MIN_MESSAGES_THRESHOLD} for auto)`);
    return;
  }

  // 去重：当前 session 已在 pending_extract.jsonl 且消息数未增加则跳过
  if (fs.existsSync(PENDING_FILE)) {
    const lines = fs.readFileSync(PENDING_FILE, 'utf8').split('\n').filter(l => l.trim());
    for (const line of lines) {
      try {
        const item = JSON.parse(line);
        if (item.session_id === sessionId && item.message_count === messages.length) {
          log(`[main] Session ${sessionId} already queued with same message count, skipping`);
          return;
        }
      } catch {}
    }
  }

  const conversation = buildConversationText(messages);

  // v1.2.8: Call amber-hunter /extract endpoint (Proactive V4)
  log('[extract] Calling amber-hunter /extract endpoint...');
  const memories = await callExtractEndpoint(conversation, sessionId, amberToken);

  if (!memories || memories.length === 0) {
    log('[extract] No memories extracted, skipping');
    return;
  }

  log(`[extract] Extracted ${memories.length} memories`);

  // Write capsules for each memory
  let written = 0;
  for (const mem of memories) {
    const summary = (mem.summary || '').trim();
    if (!summary) continue;
    const tags = ['auto-extract', mem.type || 'fact'].concat(mem.tags || []).slice(0, 5);
    const content = JSON.stringify(mem, null, 2);
    const ok = await writeCapsule(amberToken, summary, content, tags.join(','));
    if (ok) written++;
    log(`[capsule] ${ok ? '✅' : '❌'} [${mem.type}] ${summary.slice(0, 50)}`);
  }

  log(`[done] Wrote ${written}/${memories.length} capsules from ${messages.length} messages`);
}

main().catch(e => log('[error] ' + e.message));

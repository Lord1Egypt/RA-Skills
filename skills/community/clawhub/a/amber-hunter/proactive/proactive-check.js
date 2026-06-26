#!/usr/bin/env node
/**
 * amber-proactive V3.2: Zero-LLM Extraction
 * 
 * 此版本回归设计初衷：skill 脚本不调用任何外部大模型。
 * 该脚本只负责读取 session 对话并推送到 queue 中。真正的大模型提取、
 * 胶囊写入将由 agent 在其自身的 heartbeat 流程中执行。
 * 
 * 触发方式：
 * - 自动: cron 每15分钟运行此脚本 → 检查阈值 → 写 pending_extract.jsonl
 * - 手动: agent 调用此脚本（任何对话量都触发）
 * 
 * 触发阈值：
 * - 自动模式: session 消息数 ≥ 20 条
 * - 手动模式: 无限制（任意对话量）
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = os.homedir();
const SESSIONS_DIR = path.join(HOME, '.openclaw', 'agents', 'main', 'sessions');
const HUNTER_DIR = path.join(HOME, '.amber-hunter');
const PENDING_FILE = path.join(HUNTER_DIR, 'pending_extract.jsonl');
const LOG_PATH = path.join(HUNTER_DIR, 'amber-proactive.log');

const MIN_MESSAGES_THRESHOLD = 20;

// ── Logging ────────────────────────────────────────────────────────────

function log(msg) {
  const ts = new Date().toISOString().slice(11, 19);
  fs.appendFileSync(LOG_PATH, `[${ts}] ${msg}\n`);
  console.log(`[${ts}] ${msg}`);
}

// ── Session Reading ────────────────────────────────────────────────────

/**
 * Pick the session most likely to be the user's active conversation.
 *
 * Strategy: choose the session with the most messages.
 * This is more robust than mtime-based selection, because:
 * - Cron-triggered sessions typically have 1 message (just the cron trigger)
 * - Active user sessions have dozens-hundreds of messages
 * - A large session that's been idle for 30 min is still more worth capturing
 *   than a 1-message session created 1 second ago.
 */
function getActiveSession() {
  try {
    const files = fs.readdirSync(SESSIONS_DIR)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted.'))
      .map(f => {
        const fp = path.join(SESSIONS_DIR, f);
        const content = fs.readFileSync(fp, 'utf8');
        const lines = content.split('\n').filter(l => l.trim());
        let msgCount = 0;
        for (const line of lines) {
          try {
            const d = JSON.parse(line);
            if (d.type === 'message') msgCount++;
          } catch {}
        }
        return { name: f, path: fp, msgCount };
      })
      .filter(f => f.msgCount > 0)
      .sort((a, b) => b.msgCount - a.msgCount);
    return files[0] ? { path: files[0].path, id: path.basename(files[0].name, '.jsonl'), msgCount: files[0].msgCount } : null;
  } catch { return null; }
}

/**
 * Read messages from a session file.
 * Returns array of { role, text } objects.
 */
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
      if (text && text.length > 10) {
        messages.push({ role: raw.role || '?', text });
      }
    }
    return messages;
  } catch { return []; }
}

function buildConversationText(messages, maxChars = 8000) {
  const recent = messages.slice(-50);
  const text = recent.map(m => `[${m.role}]: ${m.text}`).join('\n');
  return text.length > maxChars ? text.slice(-maxChars) : text;
}

// ── Queue Management ────────────────────────────────────────────────ـــ

function writePendingExtract(sessionId, messageCount, conversation) {
  if (!fs.existsSync(HUNTER_DIR)) {
    fs.mkdirSync(HUNTER_DIR, { recursive: true });
  }
  const payload = {
    session_id: sessionId,
    message_count: messageCount,
    created_at: Math.floor(Date.now() / 1000),
    conversation: conversation
  };
  fs.appendFileSync(PENDING_FILE, JSON.stringify(payload) + '\n');
  log(`[queue] Wrote session ${sessionId} (${messageCount} msgs) to pending_extract.jsonl`);
}

// ── Main ─────────────────────────────────────────────────────────────

async function main() {
  const isManual = process.argv.includes('--manual');

  const session = getActiveSession();
  if (!session) {
    log('[main] No session file found');
    return;
  }

  const { path: sessionPath, id: sessionId, msgCount } = session;
  const messages = extractMessages(sessionPath);

  log(`[main] Session ${sessionId}: ${messages.length} messages (file has ~${msgCount})`);

  // 检查阈值
  if (!isManual && messages.length < MIN_MESSAGES_THRESHOLD) {
    log(`[main] Skipping: ${messages.length} messages (need ≥ ${MIN_MESSAGES_THRESHOLD} for auto)`);
    return;
  }

  // 去重 v1.2.33: 检查 session 是否已在队列中
  // - 若 session 已存在但消息数未增加 → 跳过（避免重复提取）
  // - 若 session 已存在且消息数增加了 → 更新队列条目（增量提取新内容）
  if (fs.existsSync(PENDING_FILE)) {
    const lines = fs.readFileSync(PENDING_FILE, 'utf8').split('\n').filter(l => l.trim());
    for (let i = 0; i < lines.length; i++) {
      try {
        const item = JSON.parse(lines[i]);
        if (item.session_id === sessionId) {
          if (item.message_count >= messages.length) {
            log(`[main] Session ${sessionId} already in queue (${item.message_count} msgs), no new messages — skipping`);
            return;
          } else {
            // 消息数增加了，更新队列条目（替换旧行）
            log(`[main] Session ${sessionId} grew ${item.message_count}→${messages.length} msgs — updating queue entry`);
            const conversation = buildConversationText(messages);
            const updated = JSON.stringify({
              session_id: sessionId,
              message_count: messages.length,
              created_at: Math.floor(Date.now() / 1000),
              conversation: conversation
            }) + '\n';
            lines[i] = updated;
            fs.writeFileSync(PENDING_FILE, lines.join('\n') + '\n');
            return;
          }
        }
      } catch {}
    }
  }

  const conversation = buildConversationText(messages);
  
  // V3.1: 将大模型提取延缓给 agent，不在此执行
  writePendingExtract(sessionId, messages.length, conversation);
}

main().catch(e => log('[error] ' + e.message));

/**
 * Dialogue Persistence — 对话持久化系统
 *
 * 管理对话历史（dialogue-history.jsonl）和梦境历史（dream-history.jsonl）
 * 的读写、查询和统计。
 *
 * 提取自 clarity.js 的 recordDialogue / getDialogueHistory /
 * getDialogueStats / getDreamHistory，v2.6.4+ 独立模块。
 *
 * @security - 所有持久化操作必须经用户明确同意
 */

const fs = require('fs');
const path = require('path');

// —— 用户同意管理 ——

let _dialoguePersistenceConsented = false;

/**
 * 设置用户是否同意对话持久化
 * @param {boolean} consented - 用户是否同意
 */
function setDialoguePersistenceConsented(consented) {
  _dialoguePersistenceConsented = !!consented;
}

/**
 * 检查用户是否已同意对话持久化
 * @returns {boolean}
 */
function isDialoguePersistenceConsented() {
  return _dialoguePersistenceConsented;
}

/**
 * 重置同意状态（用于会话结束清理）
 */
function resetDialoguePersistenceConsent() {
  _dialoguePersistenceConsented = false;
}

// —— 文件大小保护 ——

/**
 * 对话历史文件的最大允许大小（字节）
 * 超过此限制将拒绝追加写入
 */
const MAX_DIALOGUE_FILE_SIZE = 10 * 1024 * 1024; // 10MB

/**
 * 单条对话内容的最大字符数（安全裁剪上限）
 */
const MAX_CONTENT_LENGTH = 2000;

/**
 * 检查文件大小是否在允许范围内
 * @param {string} filePath - 文件路径
 * @returns {{ok: boolean, size: number, error?: string}}
 */
function checkFileSize(filePath) {
  try {
    if (!fs.existsSync(filePath)) return { ok: true, size: 0 };
    const stat = fs.statSync(filePath);
    if (stat.size > MAX_DIALOGUE_FILE_SIZE) {
      return {
        ok: false,
        size: stat.size,
        error: `文件大小 ${(stat.size / 1024 / 1024).toFixed(1)}MB 超过限制 ${MAX_DIALOGUE_FILE_SIZE / 1024 / 1024}MB`,
      };
    }
    return { ok: true, size: stat.size };
  } catch (e) {
    return { ok: false, size: 0, error: e.message };
  }
}

/**
 * 记录一条对话到永久记忆（对话历史）
 *
 * @param {object} deps - 依赖注入对象
 * @param {string} deps.rootPath - 项目根路径
 * @param {string} deps.sessionId - 当前会话 ID
 * @param {string} deps.version - 引擎版本号
 * @param {string} role - 'user' | 'clarity'
 * @param {string} content - 对话内容
 * @param {object} meta - 额外元数据（chatId, messageId 等）
 * @returns {{success: boolean, id?: string, ts?: string, error?: string}}
 */
function recordDialogue(deps, role, content, meta = {}) {
  // 安全检查：用户未明确同意时不记录
  if (!_dialoguePersistenceConsented) {
    return { success: false, error: 'persistence_not_consented' };
  }

  if (!content || !content.trim()) return { success: false, error: 'empty_content' };
  if (!['user', 'clarity'].includes(role)) role = 'unknown';

  try {
    const dir = path.join(deps.rootPath, 'memory');
    try { fs.mkdirSync(dir, { recursive: true }); } catch (e) { /* dir exists */ }
    try { fs.chmodSync(dir, 0o700); } catch (e) { /* best effort */ }
    const filePath = path.join(dir, 'dialogue-history.jsonl');

    // 安全限制：检查文件大小，超过 10MB 则拒绝写入
    const sizeCheck = checkFileSize(filePath);
    if (!sizeCheck.ok) {
      return { success: false, error: `file_size_limit: ${sizeCheck.error}` };
    }

    // 安全修剪：限制单条内容长度为 MAX_CONTENT_LENGTH
    const safeContent = typeof content === 'string'
      ? content.slice(0, MAX_CONTENT_LENGTH)
      : String(content).slice(0, MAX_CONTENT_LENGTH);

    const entry = {
      id: `msg-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      role,
      content: safeContent,
      ts: new Date().toISOString(),
      chatId: meta.chatId || null,
      meta: {
        sessionId: deps.sessionId,
        version: deps.version,
        ...meta,
      },
    };
    fs.appendFileSync(filePath, `${JSON.stringify(entry, null, 0)  }\n`, 'utf8');
    try { fs.chmodSync(filePath, 0o600); } catch (e) { /* best effort */ }
    return { success: true, id: entry.id, ts: entry.ts };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

/**
 * 查询对话历史（按时间范围）
 *
 * @param {object} deps - 依赖注入对象
 * @param {string} deps.rootPath - 项目根路径
 * @param {object} [opts] - 查询选项
 * @param {number} [opts.since] - 起始时间戳
 * @param {number} [opts.until] - 结束时间戳
 * @param {string} [opts.role] - 筛选角色
 * @param {number} [opts.limit] - 返回条数上限
 * @returns {Array<object>}
 */
function getDialogueHistory(deps, opts = {}) {
  const { since = 0, until = Date.now(), role, limit = 100 } = opts;
  const historyPath = path.join(deps.rootPath, 'memory', 'dialogue-history.jsonl');
  try {
    if (!fs.existsSync(historyPath)) return [];
    const lines = fs.readFileSync(historyPath, 'utf8').trim().split('\n').slice(-500);
    const results = [];
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const entry = JSON.parse(line);
        const ts = new Date(entry.ts).getTime();
        if (ts < since || ts > until) continue;
        if (role && entry.role !== role) continue;
        results.push(entry);
        if (results.length >= limit) break;
      } catch (e) { /* skip */ }
    }
    return results;
  } catch (e) {
    return [];
  }
}

/**
 * 获取对话统计（用于调试和报告）
 *
 * @param {object} deps - 依赖注入对象
 * @param {string} deps.rootPath - 项目根路径
 * @returns {{total: number, user?: number, clarity?: number, fileSize?: string, byRole?: object}}
 */
function getDialogueStats(deps) {
  const historyPath = path.join(deps.rootPath, 'memory', 'dialogue-history.jsonl');
  try {
    if (!fs.existsSync(historyPath)) return { total: 0, user: 0, clarity: 0, fileSize: 0 };
    const stat = fs.statSync(historyPath);
    const lines = fs.readFileSync(historyPath, 'utf8').trim().split('\n');
    const byRole = { user: 0, clarity: 0, unknown: 0 };
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const entry = JSON.parse(line);
        byRole[entry.role] = (byRole[entry.role] || 0) + 1;
      } catch (e) { /* skip */ }
    }
    return {
      total: lines.filter(l => l.trim()).length,
      byRole,
      fileSize: `${(stat.size / 1024).toFixed(1)} KB`,
      lastEntry: lines.filter(l => l.trim()).slice(-1)[0]
        ? (() => { try { return JSON.parse(lines.filter(l => l.trim()).slice(-1)[0]).ts; } catch { return null; } })()
        : null,
    };
  } catch (e) {
    return { total: 0, error: e.message };
  }
}

/**
 * 获取梦境历史摘要
 *
 * @param {object} deps - 依赖注入对象
 * @param {string} deps.rootPath - 项目根路径
 * @param {number} [limit=10] - 返回条数上限
 * @returns {Array<object>}
 */
function getDreamHistory(deps, limit = 10) {
  const historyPath = path.join(deps.rootPath, 'memory', 'dream-history.jsonl');
  try {
    if (!fs.existsSync(historyPath)) return [];
    const lines = fs.readFileSync(historyPath, 'utf8').trim().split('\n').slice(-limit);
    return lines.map(line => {
      try { return JSON.parse(line); } catch { return null; }
    }).filter(Boolean).reverse();
  } catch (e) {
    return [];
  }
}

module.exports = {
  recordDialogue,
  getDialogueHistory,
  getDialogueStats,
  getDreamHistory,
  setDialoguePersistenceConsented,
  isDialoguePersistenceConsented,
  resetDialoguePersistenceConsent,
  checkFileSize,
  MAX_DIALOGUE_FILE_SIZE,
  MAX_CONTENT_LENGTH,
};

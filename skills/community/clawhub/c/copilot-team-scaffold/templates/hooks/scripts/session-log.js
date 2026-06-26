#!/usr/bin/env node
'use strict';
// 会话审计日志共享模块 — 供所有 hook 脚本记录事件

const fs = require('fs');
const path = require('path');

const LOG_DIR = '.github/session-logs';
const MAX_LOG_FILES = 100;
const MAX_AGE_DAYS = 30;

/** 获取当前会话的日志文件路径（基于 sessionId 或时间戳） */
function getLogFile(sessionId) {
  if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
  }

  // 使用 sessionId 的前 8 位 + 日期作为文件名
  const date = new Date().toISOString().slice(0, 10);
  const sid = sessionId ? sessionId.slice(0, 8) : 'unknown';
  return path.join(LOG_DIR, `${date}_${sid}.md`);
}

/** 追加一条日志条目 */
function appendLog(sessionId, event, details) {
  try {
    const logFile = getLogFile(sessionId);
    const time = new Date().toISOString().slice(11, 19);

    // 如果文件不存在，写入头部
    if (!fs.existsSync(logFile)) {
      const header = `# Session ${new Date().toISOString().slice(0, 19).replace('T', ' ')}\n\n`;
      fs.writeFileSync(logFile, header, 'utf8');
    }

    // 构建条目
    const lines = [`## ${time} | ${event}`];
    for (const [key, value] of Object.entries(details)) {
      if (value !== undefined && value !== null && value !== '') {
        lines.push(`- **${key}**: ${value}`);
      }
    }
    lines.push('');

    fs.appendFileSync(logFile, lines.join('\n') + '\n', 'utf8');
  } catch {
    // 日志写入失败不阻塞主流程
  }
}

/** 清理过期日志文件和旧重试计数器 */
function cleanupLogs() {
  try {
    if (!fs.existsSync(LOG_DIR)) return;

    const files = fs.readdirSync(LOG_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => ({ name: f, full: path.join(LOG_DIR, f), mtime: fs.statSync(path.join(LOG_DIR, f)).mtimeMs }))
      .sort((a, b) => b.mtime - a.mtime);

    const cutoff = Date.now() - MAX_AGE_DAYS * 86400000;

    for (let i = 0; i < files.length; i++) {
      if (i >= MAX_LOG_FILES || files[i].mtime < cutoff) {
        try { fs.unlinkSync(files[i].full); } catch {}
      }
    }

    // 清理旧的 .retry-* 计数器文件（超过 1 天的）
    const retryCutoff = Date.now() - 86400000;
    const retryFiles = fs.readdirSync(LOG_DIR).filter(f => f.startsWith('.retry-'));
    for (const f of retryFiles) {
      const full = path.join(LOG_DIR, f);
      try {
        if (fs.statSync(full).mtimeMs < retryCutoff) fs.unlinkSync(full);
      } catch {}
    }
  } catch {}
}

module.exports = { getLogFile, appendLog, cleanupLogs, LOG_DIR };

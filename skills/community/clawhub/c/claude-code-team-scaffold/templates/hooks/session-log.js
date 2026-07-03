#!/usr/bin/env node
'use strict';
// Session audit log — append-only markdown log of all hook events.

const fs = require('fs');
const path = require('path');
const { SESSION_LOG_DIR } = require('./paths');

const MAX_LOG_FILES = 100;
const MAX_AGE_DAYS = 30;

function ensureLogDir() {
  if (!fs.existsSync(SESSION_LOG_DIR)) {
    fs.mkdirSync(SESSION_LOG_DIR, { recursive: true });
  }
}

function getLogFile(sessionId) {
  ensureLogDir();
  const date = new Date().toISOString().slice(0, 10);
  const sid = sessionId ? String(sessionId).slice(0, 8) : 'unknown';
  return path.join(SESSION_LOG_DIR, `${date}_${sid}.md`);
}

function appendLog(sessionId, event, details) {
  try {
    const logFile = getLogFile(sessionId);
    const now = new Date();
    const timestamp = now.toISOString().slice(0, 19).replace('T', ' ');

    if (!fs.existsSync(logFile)) {
      const header = `# Session ${timestamp}\n\n`;
      fs.writeFileSync(logFile, header, 'utf8');
    }

    const entry = `## ${now.toISOString()} | ${event}\n\n` +
      '```json\n' +
      JSON.stringify(details || {}, null, 2) +
      '\n```\n\n';

    fs.appendFileSync(logFile, entry, 'utf8');
  } catch {
    // Logging failure must never break the hook.
  }
}

function cleanupLogs() {
  try {
    if (!fs.existsSync(SESSION_LOG_DIR)) return;

    const files = fs.readdirSync(SESSION_LOG_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => ({
        name: f,
        full: path.join(SESSION_LOG_DIR, f),
        mtime: fs.statSync(path.join(SESSION_LOG_DIR, f)).mtimeMs,
      }))
      .sort((a, b) => b.mtime - a.mtime);

    const cutoff = Date.now() - MAX_AGE_DAYS * 86400000;

    for (let i = 0; i < files.length; i++) {
      if (i >= MAX_LOG_FILES || files[i].mtime < cutoff) {
        try { fs.unlinkSync(files[i].full); } catch {}
      }
    }
  } catch {}
}

module.exports = { getLogFile, appendLog, cleanupLogs, SESSION_LOG_DIR };

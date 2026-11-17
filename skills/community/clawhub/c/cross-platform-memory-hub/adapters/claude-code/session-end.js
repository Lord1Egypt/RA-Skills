#!/usr/bin/env node
/**
 * Safe template: session-end.js
 * Default behavior: no write unless user has explicitly enabled it with MEMORY_HUB_USER_CONFIRMED=1 and MEMORY_HUB_ENABLE_WRITE=1.
 * The script only stores user-provided MEMORY_HUB_* summary fields; it does not read raw session text.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const ENABLED = process.env.MEMORY_HUB_USER_CONFIRMED === '1' && process.env.MEMORY_HUB_ENABLE_WRITE === '1';
const OBSIDIAN_PATHS = [
  process.env.OBSIDIAN_PATH_PRIMARY,
  process.env.OBSIDIAN_PATH_SECONDARY,
  'L:/Obsidian',
  'E:/Obsidian',
  path.join(os.homedir(), 'Documents/Obsidian'),
  path.join(os.homedir(), 'Obsidian')
].filter(Boolean);

function getToday() {
  return new Date().toISOString().slice(0, 10);
}

function getNow() {
  return new Date().toISOString().slice(0, 19).replace('T', ' ');
}

function findObsidianRoot() {
  for (const candidate of OBSIDIAN_PATHS) {
    if (fs.existsSync(path.join(candidate, '.obsidian'))) return candidate;
  }
  return null;
}

function sanitize(value) {
  return String(value || '')
    .replace(/(token|secret|password|key)\s*[:=]\s*\S+/gi, '$1=[REDACTED]')
    .replace(/-----BEGIN[\s\S]*?-----END[^-]+-----/g, '[REDACTED_KEY_BLOCK]');
}

function main() {
  if (!ENABLED) {
    console.log('[memory-hub] write disabled. Set MEMORY_HUB_USER_CONFIRMED=1 and MEMORY_HUB_ENABLE_WRITE=1 after user consent.');
    return;
  }

  const root = findObsidianRoot();
  if (!root) {
    console.error('[memory-hub] no valid Obsidian vault found.');
    return;
  }

  const summary = sanitize(process.env.MEMORY_HUB_SUMMARY || 'User did not provide a summary.');
  const tasks = sanitize(process.env.MEMORY_HUB_PENDING_TASKS || '');
  const decisions = sanitize(process.env.MEMORY_HUB_DECISIONS || '');
  const blockers = sanitize(process.env.MEMORY_HUB_BLOCKERS || '');

  const diaryDir = path.join(root, '开发日志', '工作日记');
  const diaryFile = path.join(diaryDir, `${getToday()}.md`);
  fs.mkdirSync(diaryDir, { recursive: true });

  const content = `
## 用户授权会话摘要 - ${getNow()}

### 摘要
${summary}

### 待办
${tasks}

### 决策
${decisions}

### 风险
${blockers}

---
`;
  fs.appendFileSync(diaryFile, content, 'utf-8');
  console.log(`[memory-hub] saved user-confirmed summary to ${diaryFile}`);
}

main();
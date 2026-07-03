#!/usr/bin/env node
'use strict';
// PostToolUse handler — track CLAUDE.md reads, track edits, soft reminders.

const fs = require('fs');
const path = require('path');
const {
  GATE_FILE, EDITS_FILE, findModuleClaudeMd, PROJECT_ROOT,
} = require('./paths');

const WRITE_TOOLS = new Set(['Edit', 'Write', 'MultiEdit']);
const CLAUDE_MD_RE = /(^|\/)(CLAUDE|AGENTS)\.md$/i;

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write(''); }
});

function loadJson(p, fallback) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); }
  catch { return fallback; }
}

function saveJson(p, obj) {
  try {
    const dir = path.dirname(p);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(p, JSON.stringify(obj, null, 2), 'utf8');
  } catch {}
}

function dedupPush(arr, item) {
  if (!arr.some(x => (x.path || x) === (item.path || item))) arr.push(item);
}

function extractFilePath(toolName, params) {
  if (!params) return '';
  if (toolName === 'MultiEdit') {
    const edits = params.edits || params.replacements || [];
    return edits[0] ? (edits[0].file_path || edits[0].filePath || '') : '';
  }
  return params.file_path || params.filePath || '';
}

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch {}
  const toolName = data.tool_name || '';
  const params = data.tool_input || {};
  const cwd = data.cwd || PROJECT_ROOT;

  if (toolName === 'Read') {
    const filePath = params.file_path || params.filePath || '';
    if (filePath && CLAUDE_MD_RE.test(filePath)) {
      const gate = loadJson(GATE_FILE, { readFiles: [] });
      const readFiles = gate.readFiles || [];
      if (!readFiles.includes(filePath)) readFiles.push(filePath);
      saveJson(GATE_FILE, { ...gate, readFiles });
    }
    return;
  }

  if (!WRITE_TOOLS.has(toolName)) return;

  const filePath = extractFilePath(toolName, params);
  if (!filePath) return;

  const edits = loadJson(EDITS_FILE, { codeChanges: [], claudeMdChanges: [] });
  if (CLAUDE_MD_RE.test(filePath)) {
    dedupPush(edits.claudeMdChanges || (edits.claudeMdChanges = []), { path: filePath, timestamp: new Date().toISOString() });
  } else {
    dedupPush(edits.codeChanges || (edits.codeChanges = []), { path: filePath, timestamp: new Date().toISOString() });
  }
  saveJson(EDITS_FILE, edits);

  // Soft reminder for Write into a module root with no CLAUDE.md.
  if (toolName === 'Write') {
    const parent = path.dirname(filePath);
    if (!findModuleClaudeMd(filePath, cwd) && !fs.existsSync(path.join(cwd, parent, 'CLAUDE.md'))) {
      const tracked = (edits.codeChanges || []).length === 1;
      if (tracked) {
        process.stdout.write(`[soft reminder] Created ${filePath} in ${parent.replace(/\\/g, '/')} with no CLAUDE.md.\n`);
      }
    }
  }
}

process.stdin.resume();

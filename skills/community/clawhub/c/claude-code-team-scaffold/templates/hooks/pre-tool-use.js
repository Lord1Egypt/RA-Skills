#!/usr/bin/env node
'use strict';
// PreToolUse handler — CLAUDE.md gate, applyTo instructions injection, project memory.

const fs = require('fs');
const path = require('path');
const {
  GATE_FILE, INSTRUCTIONS_DIR, MEMORY_PROJECT_DIR,
  findModuleClaudeMd, isInModuleRoot, PROJECT_ROOT,
} = require('./paths');

const WRITE_TOOLS = new Set(['Edit', 'Write', 'MultiEdit']);
const CLAUDE_MD_RE = /(^|\/)(CLAUDE|AGENTS)\.md$/i;

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function safeRead(p) {
  try { return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : ''; }
  catch { return ''; }
}

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

function extractFilePath(toolName, params) {
  if (!params) return '';
  if (toolName === 'MultiEdit') {
    const edits = params.edits || params.replacements || [];
    return edits[0] ? (edits[0].file_path || edits[0].filePath || '') : '';
  }
  return params.file_path || params.filePath || '';
}

/** Minimal glob matcher: supports *, **, ? — good enough for applyTo patterns. */
function globMatch(pattern, str) {
  let regex = '^';
  let i = 0;
  while (i < pattern.length) {
    const c = pattern[i];
    if (c === '*') {
      if (pattern[i + 1] === '*') {
        regex += '.*';
        i += 2;
        if (pattern[i] === '/') i++;
      } else {
        regex += '[^/]*';
        i++;
      }
    } else if (c === '?') {
      regex += '[^/]';
      i++;
    } else if ('.+^$()|{}[]\\'.includes(c)) {
      regex += '\\' + c;
      i++;
    } else {
      regex += c;
      i++;
    }
  }
  regex += '$';
  return new RegExp(regex).test(str);
}

function parseApplyTo(content) {
  const m = content.match(/^applyTo:\s*(.+)$/m);
  if (!m) return null;
  return m[1].trim().replace(/^["']|["']$/g, '');
}

function readApplyToMatches(filePath) {
  if (!fs.existsSync(INSTRUCTIONS_DIR)) return [];
  let entries = [];
  try { entries = fs.readdirSync(INSTRUCTIONS_DIR); } catch { return []; }
  const normalized = filePath.replace(/\\/g, '/');
  const matches = [];
  for (const name of entries) {
    if (!name.endsWith('.md')) continue;
    const full = path.join(INSTRUCTIONS_DIR, name);
    const content = safeRead(full);
    if (!content) continue;
    const pattern = parseApplyTo(content);
    if (!pattern) continue;
    if (globMatch(pattern, normalized)) matches.push(content);
  }
  return matches;
}

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch {}
  const toolName = data.tool_name || '';
  const params = data.tool_input || {};
  const cwd = data.cwd || PROJECT_ROOT;

  if (!WRITE_TOOLS.has(toolName)) {
    process.stdout.write('{}');
    return;
  }

  const filePath = extractFilePath(toolName, params);
  if (!filePath) {
    process.stdout.write('{}');
    return;
  }

  const additionalContext = [];

  // --- CLAUDE.md gate check ---
  const gate = loadJson(GATE_FILE, { readFiles: [] });
  const readSet = new Set(gate.readFiles || []);
  if (!readSet.has(filePath)) {
    const moduleMd = findModuleClaudeMd(filePath, cwd);
    if (moduleMd) {
      additionalContext.push(
        `[claude-md-gate] You have not read ${moduleMd} this session. ` +
        `Read it before editing ${filePath} to understand module conventions.`
      );
    } else if (isInModuleRoot(filePath, cwd)) {
      const dirMatch = filePath.match(/^(.*?)\//);
      const dir = dirMatch ? dirMatch[1] : filePath;
      process.stdout.write(JSON.stringify({
        decision: 'block',
        reason: `Module ${dir} has no CLAUDE.md. Create one first.`,
      }));
      return;
    }
  }

  // --- applyTo instructions injection ---
  const applied = readApplyToMatches(filePath);
  for (const content of applied) additionalContext.push(content);

  // --- Project memory injection when writing CLAUDE.md / AGENTS.md ---
  if (toolName === 'Write' && CLAUDE_MD_RE.test(filePath)) {
    for (const name of ['code-style.md', 'execution-discipline.md']) {
      const p = path.join(MEMORY_PROJECT_DIR, name);
      const content = safeRead(p);
      if (content) additionalContext.push(`--- ${name} ---\n${content}`);
    }
  }

  if (additionalContext.length === 0) {
    process.stdout.write('{}');
    return;
  }

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      additionalContext: additionalContext.join('\n\n'),
    },
    decision: 'approve',
  }));
}

process.stdin.resume();

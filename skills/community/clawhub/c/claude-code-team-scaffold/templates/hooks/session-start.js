#!/usr/bin/env node
'use strict';
// SessionStart handler — initialize gate/edits files, inject memory + lessons.

const fs = require('fs');
const path = require('path');
const {
  GATE_FILE, EDITS_FILE, LESSONS_FILE,
  MEMORY_GLOBAL_DIR, MEMORY_PROJECT_DIR, GLOBAL_CLAUDE_MD,
  RUNTIME_DIR,
} = require('./paths');
const { cleanupLogs } = require('./session-log');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write(''); }
});

function safeRead(p) {
  try { return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : ''; }
  catch { return ''; }
}

function listMarkdown(dir) {
  try {
    if (!fs.existsSync(dir)) return [];
    return fs.readdirSync(dir)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(dir, f))
      .sort();
  } catch { return []; }
}

function readDirSection(title, dir) {
  const files = listMarkdown(dir);
  if (files.length === 0) return '';
  const parts = [`=== ${title} ===`];
  for (const f of files) {
    parts.push(`--- ${path.basename(f)} ---`);
    parts.push(safeRead(f));
  }
  return parts.join('\n');
}

function readLastLessons(file, count) {
  const content = safeRead(file);
  if (!content) return '';
  const sections = content.split(/(?=^## \d{4}-)/m).slice(1, count + 1);
  if (sections.length === 0) return '';
  return `=== Recent Lessons (last ${sections.length}) ===\n` + sections.join('\n');
}

function ensureJson(file, fallback) {
  try {
    if (!fs.existsSync(RUNTIME_DIR)) fs.mkdirSync(RUNTIME_DIR, { recursive: true });
    if (!fs.existsSync(file)) {
      fs.writeFileSync(file, JSON.stringify(fallback, null, 2), 'utf8');
    } else {
      JSON.parse(fs.readFileSync(file, 'utf8'));
    }
  } catch {
    try { fs.writeFileSync(file, JSON.stringify(fallback, null, 2), 'utf8'); } catch {}
  }
}

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch {}
  const sessionId = data.session_id || '';

  // Initialize gate + edits files.
  ensureJson(GATE_FILE, { readFiles: [] });
  ensureJson(EDITS_FILE, { codeChanges: [], claudeMdChanges: [] });

  // Clean up stale logs.
  cleanupLogs();

  const sections = [
    readDirSection('Project Memory', MEMORY_PROJECT_DIR),
    readDirSection('Global Memory', MEMORY_GLOBAL_DIR),
  ];

  const globalClaude = safeRead(GLOBAL_CLAUDE_MD);
  if (globalClaude) {
    sections.push('=== Global CLAUDE.md ===\n' + globalClaude);
  }

  const lessons = readLastLessons(LESSONS_FILE, 5);
  if (lessons) sections.push(lessons);

  const context = sections.filter(Boolean).join('\n\n');
  if (context) process.stdout.write(context + '\n');

  // Log via session-log utility.
  try {
    const { appendLog } = require('./session-log');
    appendLog(sessionId, 'session_start', { session_id: sessionId });
  } catch {}
}

process.stdin.resume();

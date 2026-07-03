#!/usr/bin/env node
'use strict';
// Stop handler — CLAUDE.md sync check + spec-flow summary + log session_stop.

const fs = require('fs');
const path = require('path');
const {
  GATE_FILE, EDITS_FILE, SPEC_FLOW_ACTIVE_DIR,
  findModuleClaudeMd, PROJECT_ROOT,
} = require('./paths');
const { appendLog } = require('./session-log');

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function safeExists(p) { try { return fs.existsSync(p); } catch { return false; } }

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

function checkCodeModuleSync() {
  const edits = loadJson(EDITS_FILE, { codeChanges: [], claudeMdChanges: [] });
  const codeChanges = edits.codeChanges || [];
  const claudeMdChanges = edits.claudeMdChanges || [];
  if (codeChanges.length === 0 || claudeMdChanges.length > 0) return null;

  const missing = [];
  for (const c of codeChanges) {
    const p = (c.path || c).replace(/\\/g, '/');
    if (findModuleClaudeMd(p, PROJECT_ROOT)) missing.push(p);
  }
  if (missing.length === 0) return null;

  return `Code changed in modules with CLAUDE.md, but CLAUDE.md was not updated. ` +
    `Update module CLAUDE.md to reflect changes before stopping.\n` +
    missing.map(m => '  - ' + m).join('\n');
}

function scanSpecFlowInProgress() {
  if (!safeExists(SPEC_FLOW_ACTIVE_DIR)) return '';
  let entries = [];
  try { entries = fs.readdirSync(SPEC_FLOW_ACTIVE_DIR); } catch { return ''; }
  const lines = [];
  for (const e of entries) {
    const tasksFile = path.join(SPEC_FLOW_ACTIVE_DIR, e, 'tasks.md');
    if (!safeExists(tasksFile)) continue;
    let content = '';
    try { content = fs.readFileSync(tasksFile, 'utf8'); } catch { continue; }
    const inProgress = (content.match(/\[in_progress\]/g) || []).length;
    const pending = (content.match(/\[pending\]/g) || []).length;
    const complete = (content.match(/\[complete\]/g) || []).length;
    if (inProgress > 0) {
      lines.push(`[spec-flow] ${e}: ${inProgress} in_progress, ${pending} pending, ${complete} complete`);
    }
  }
  return lines.join('\n');
}

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch {}
  if (data.stop_hook_active === true) { process.stdout.write('{}'); return; }

  const sessionId = data.session_id || '';

  const syncWarning = checkCodeModuleSync();
  const specSummary = scanSpecFlowInProgress();
  if (specSummary) process.stdout.write(specSummary + '\n');

  appendLog(sessionId, 'session_stop', {
    duration_sec: data.duration_sec || 0,
    total_events: data.total_events || 0,
  });

  // Reset gate for next session.
  const gate = loadJson(GATE_FILE, { readFiles: [] });
  saveJson(GATE_FILE, { ...gate, readFiles: [] });

  if (syncWarning) {
    process.stdout.write(JSON.stringify({
      decision: 'block',
      reason: syncWarning,
    }));
    return;
  }

  process.stdout.write('{}');
}

process.stdin.resume();

#!/usr/bin/env node
'use strict';
// Post-tool-use lint hook — auto-runs linter after file edits.
// Supports: ruff (Python), eslint (TS/TSX). Add more as needed.
// Uses windowsHide to avoid console windows on Windows/RemoteApp.

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch {}
  process.exit(0);
});

function run() {
  let data;
  try { data = JSON.parse(input); } catch { return; }

  const toolName = data.tool_name || data.toolName || '';
  if (!['create_file', 'replace_string_in_file', 'multi_replace_string_in_file'].includes(toolName)) return;

  const params = data.tool_input || data.toolInput || data.input || {};
  let filePath = params.filePath || params.file_path || '';
  if (!filePath && Array.isArray(params.replacements) && params.replacements[0]) {
    filePath = params.replacements[0].filePath || '';
  }
  if (!filePath) return;

  const ext = path.extname(filePath);

  if (ext === '.py') {
    try {
      execFileSync('ruff', ['check', '--fix', '--quiet', filePath], {
        encoding: 'utf8', timeout: 10000, windowsHide: true,
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    } catch {}
  } else if (ext === '.ts' || ext === '.tsx') {
    const eslintBin = path.join('frontend', 'node_modules', '.bin', 'eslint');
    if (fs.existsSync(eslintBin)) {
      try {
        execFileSync('npx', ['eslint', '--fix', filePath], {
          encoding: 'utf8', timeout: 10000, windowsHide: true,
          cwd: 'frontend',
          stdio: ['pipe', 'pipe', 'pipe'],
        });
      } catch {}
    }
  }
}

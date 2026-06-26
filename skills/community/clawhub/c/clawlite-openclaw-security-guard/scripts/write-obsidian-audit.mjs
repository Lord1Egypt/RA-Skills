#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const [,, jsonPath, noteTitle] = process.argv;
if (!jsonPath) {
  console.error('Usage: node write-obsidian-audit.mjs <audit-json-path> [note-title]');
  process.exit(2);
}
const vaultDir = '/Users/m1/Desktop/obsidianvault/ClawLite';
const outDir = path.join(vaultDir, 'Security Audits');
fs.mkdirSync(outDir, { recursive: true });
const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
const ts = new Date().toISOString().replace(/[:.]/g, '-');
const title = noteTitle || `Security Audit ${ts}`;
const outPath = path.join(outDir, `${title}.md`);
const lines = [];
lines.push(`# ${title}`);
lines.push('');
lines.push(`- Root: ${data.root}`);
lines.push(`- Verdict: ${data.verdict}`);
lines.push(`- Findings: ${(data.findings || []).length}`);
lines.push('');
for (const f of (data.findings || [])) {
  lines.push(`- [${f.level}] ${f.label} — ${f.file}:${f.line}`);
  lines.push(`  - ${f.excerpt}`);
}
fs.writeFileSync(outPath, lines.join('\n'));
console.log(outPath);

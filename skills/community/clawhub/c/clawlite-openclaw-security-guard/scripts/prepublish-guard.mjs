#!/usr/bin/env node
import { spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const skillDir = process.argv[2];
if (!skillDir) {
  console.error('Usage: node prepublish-guard.mjs <skill-dir>');
  process.exit(2);
}
const abs = path.resolve(skillDir);
const auditScript = path.resolve(path.dirname(new URL(import.meta.url).pathname), 'audit-skill-dir.mjs');
const result = spawnSync(process.execPath, [auditScript, abs], { encoding: 'utf8' });
if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
let parsed;
try { parsed = JSON.parse(result.stdout || '{}'); } catch { parsed = null; }
if (!parsed) process.exit(1);
const actionableBlocks = (parsed.findings || []).filter(f => f.level === 'BLOCK' && !/references\/checklist\.md|scripts\/audit-skill-dir\.mjs|scripts\/security-check\.mjs/.test(f.file));
if (actionableBlocks.length > 0) {
  console.error('\nPrepublish guard: BLOCK due to actionable findings.');
  process.exit(1);
}
console.log('\nPrepublish guard: PASS (no actionable BLOCK findings).');

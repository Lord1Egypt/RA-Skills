#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const workspace = '/home/admin/.openclaw/workspace';
const singleScript = path.join(workspace, 'bin', 'merge_feishu_identity.js');

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

const inputPath = process.argv[2];
if (!inputPath) fail('Usage: node bin/merge_feishu_identity_batch.js <json-file>');

const resolved = path.isAbsolute(inputPath) ? inputPath : path.join(workspace, inputPath);
if (!fs.existsSync(resolved)) fail(`Input file not found: ${resolved}`);

const raw = fs.readFileSync(resolved, 'utf8');
const records = JSON.parse(raw);
if (!Array.isArray(records)) fail('Input JSON must be an array of records');

const results = [];
for (const rec of records) {
  const out = spawnSync(process.execPath, [singleScript, JSON.stringify(rec)], { encoding: 'utf8' });
  results.push({
    record: rec,
    code: out.status,
    stdout: out.stdout.trim(),
    stderr: out.stderr.trim()
  });
}

const summary = {
  ok: results.every(r => r.code === 0),
  total: results.length,
  succeeded: results.filter(r => r.code === 0).length,
  failed: results.filter(r => r.code !== 0).length,
  results
};

console.log(JSON.stringify(summary, null, 2));
if (!summary.ok) process.exit(2);

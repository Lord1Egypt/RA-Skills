const fs = require('fs');
const path = require('path');

const WORKSPACE = process.argv[2] || process.env.WORKSPACE_ROOT || process.cwd();
const SESSION_GLOB = '**/*.jsonl';
const MAX_EXEC_RATIO_DEFAULT = 0.35;
const MAX_REPEATED_EXEC_DEFAULT = 3;

function exists(file) {
  try { return fs.existsSync(file); } catch { return false; }
}

function findJsonlFiles(root) {
  const results = [];
  const walk = (dir) => {
    if (!exists(dir)) return;
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.name.startsWith('.') && entry.name !== '.') continue;
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile() && full.endsWith('.jsonl')) results.push(full);
    }
  };
  walk(root);
  return results;
}

function extractToolCalls(line) {
  const hits = [];
  if (!line || typeof line !== 'string') return hits;
  const regex = /\[TOOL:\s*([^\]]+)\]/g;
  let m;
  while ((m = regex.exec(line))) hits.push(m[1].trim());
  return hits;
}

function countToolUsage(files) {
  const counts = new Map();
  for (const file of files) {
    let text;
    try { text = fs.readFileSync(file, 'utf8'); } catch { continue; }
    for (const line of text.split(/\r?\n/)) {
      for (const tool of extractToolCalls(line)) counts.set(tool, (counts.get(tool) || 0) + 1);
    }
  }
  return counts;
}

function analyze(execCount, totalCount, repeatedExecFiles) {
  const total = totalCount || execCount || 0;
  const ratio = total > 0 ? execCount / total : 0;
  const issues = [];
  if (ratio > MAX_EXEC_RATIO_DEFAULT) issues.push({ severity: 'medium', text: `high_exec_ratio=${ratio.toFixed(2)}` });
  if (repeatedExecFiles.length >= 1) issues.push({ severity: 'low', text: `repeated_exec_patterns=${repeatedExecFiles.length}` });
  return { ratio, issues };
}

function main() {
  const files = findJsonlFiles(WORKSPACE);
  const counts = countToolUsage(files);
  const execCount = counts.get('exec') || 0;
  const shellCount = counts.get('shell') || 0;
  const totalCount = Array.from(counts.values()).reduce((a, b) => a + b, 0);
  const repeatedExecFiles = files.filter(file => {
    let text;
    try { text = fs.readFileSync(file, 'utf8'); } catch { return false; }
    let execs = 0;
    for (const line of text.split(/\r?\n/)) {
      if (/\[TOOL:\s*exec\]/.test(line)) execs++;
      if (/\[TOOL:\s*sudo\]/.test(line)) return true;
      if (/admin/i.test(line) && /\[TOOL:\s*exec\]/.test(line)) return true;
    }
    return execs > MAX_REPEATED_EXEC_DEFAULT;
  });

  const { ratio, issues } = analyze(execCount + shellCount, totalCount, repeatedExecFiles);
  const riskCount = issues.length;
  const status = riskCount === 0 ? 'PASS' : riskCount < 3 ? 'WARN' : 'FAIL';

  console.log(`=== Exec Policy Enforcer ===`);
  console.log(`Workspace: ${WORKSPACE}`);
  console.log(`Status: ${status}`);
  console.log(`exec=${execCount} shell=${shellCount} total_tool_calls=${totalCount}`);
  console.log(`exec_ratio=${ratio.toFixed(3)}`);
  console.log(`Risky files: ${repeatedExecFiles.length}`);
  for (const issue of issues) console.log(`- [${issue.severity.toUpperCase()}] ${issue.text}`);
  return status;
}

if (require.main === module) {
  process.exit(main() === 'PASS' ? 0 : 1);
}

module.exports = { main };

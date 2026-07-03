#!/usr/bin/env node
'use strict';
// SubagentStop handler — quality gate: lint + type-check + related tests.
// On failure: block with retry hint. After 3 retries: degrade to log only.

const fs = require('fs');
const path = require('path');
const { execFileSync, execSync } = require('child_process');
const {
  RETRY_FILE, RUNTIME_DIR, LESSONS_FILE, PROJECT_ROOT,
} = require('./paths');
const { appendLog } = require('./session-log');

const MAX_RETRIES = 3;

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function safeExists(p) { try { return fs.existsSync(p); } catch { return false; } }

function truncate(s, n) {
  s = String(s || '');
  return s.length > n ? s.slice(0, n) + '\n... (truncated)' : s;
}

function getChangedFiles() {
  try {
    const out = execSync('git diff --name-only HEAD', {
      encoding: 'utf8', timeout: 10000, windowsHide: true,
      stdio: ['pipe', 'pipe', 'pipe'], cwd: PROJECT_ROOT,
    }).trim();
    return out.split('\n').map(s => s.trim()).filter(Boolean)
      .filter(f => safeExists(path.resolve(PROJECT_ROOT, f)));
  } catch {
    return [];
  }
}

function tryCmd(cmd, args, opts) {
  try {
    execFileSync(cmd, args, { encoding: 'utf8', windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'], ...opts });
    return { ok: true };
  } catch (e) {
    const out = (e.stdout || '') + (e.stderr || '');
    // ENOENT (tool missing) returns empty out.
    return { ok: false, output: out, code: e.status };
  }
}

function runRuff(files) {
  const r = tryCmd('ruff', ['check', ...files], { timeout: 30000, cwd: PROJECT_ROOT });
  if (r.ok || !r.output.trim()) return null;
  return `**ruff:**\n\`\`\`\n${truncate(r.output, 500)}\n\`\`\``;
}

function runPyright(files) {
  const r = tryCmd('pyright', [...files], { timeout: 60000, cwd: PROJECT_ROOT });
  if (r.ok || !r.output.trim()) return null;
  return `**pyright:**\n\`\`\`\n${truncate(r.output, 500)}\n\`\`\``;
}

function runTsc() {
  // Run only if a tsconfig.json exists somewhere in the project.
  if (!safeExists(path.join(PROJECT_ROOT, 'tsconfig.json'))) return null;
  const r = tryCmd('npx', ['tsc', '--noEmit'], { timeout: 120000, cwd: PROJECT_ROOT });
  if (r.ok || !r.output.trim()) return null;
  const lines = r.output.split('\n').filter(l => l.includes('error TS')).slice(0, 10).join('\n');
  return lines ? `**tsc:**\n\`\`\`\n${lines}\n\`\`\`` : null;
}

function runEslint(files) {
  const r = tryCmd('npx', ['eslint', ...files], { timeout: 60000, cwd: PROJECT_ROOT });
  if (r.ok || !r.output.trim()) return null;
  return `**eslint:**\n\`\`\`\n${truncate(r.output, 500)}\n\`\`\``;
}

/** Map foo.py → test_foo.py beside it, or in tests/ sibling. */
function pythonTestsFor(f) {
  if (!f.endsWith('.py') || f.includes('__pycache__')) return [];
  const base = path.basename(f);
  if (base.startsWith('__')) return [];
  const dir = path.dirname(f);
  const candidate = path.join(dir, `test_${base}`);
  if (safeExists(candidate)) return [candidate];
  const testsDir = path.join(dir, '..', 'tests');
  const inTests = path.join(testsDir, `test_${base}`);
  return safeExists(inTests) ? [inTests] : [];
}

/** Map Foo.tsx → Foo.test.tsx beside it. */
function tsTestsFor(f) {
  if (!(f.endsWith('.ts') || f.endsWith('.tsx'))) return [];
  if (f.includes('.test.') || f.includes('__tests__')) return [];
  const dir = path.dirname(f);
  const ext = path.extname(f);
  const base = path.basename(f, ext);
  const candidate = path.join(dir, `${base}.test${ext}`);
  return safeExists(candidate) ? [candidate] : [];
}

function runPytest(files) {
  if (files.length === 0) return null;
  const r = tryCmd('python', ['-m', 'pytest', '-x', '--tb=short', '-q', ...files], { timeout: 90000, cwd: PROJECT_ROOT });
  if (r.ok) return null;
  if (r.output.includes('FAILED') || r.output.includes('ERROR')) {
    return `**pytest:**\n\`\`\`\n${truncate(r.output, 800)}\n\`\`\``;
  }
  return null;
}

function runVitest(files) {
  if (files.length === 0) return null;
  const r = tryCmd('npx', ['vitest', 'run', ...files], { timeout: 90000, cwd: PROJECT_ROOT });
  if (r.ok) return null;
  if (r.output.includes('FAIL') || r.output.includes('Error')) {
    return `**vitest:**\n\`\`\`\n${truncate(r.output, 800)}\n\`\`\``;
  }
  return null;
}

function retryKey(filePath) {
  return filePath.replace(/[^a-zA-Z0-9._-]/g, '_');
}

function getRetry(filePath) {
  const data = loadJson(RETRY_FILE, {});
  return data[retryKey(filePath)] || 0;
}

function bumpRetry(filePath) {
  try {
    if (!fs.existsSync(RUNTIME_DIR)) fs.mkdirSync(RUNTIME_DIR, { recursive: true });
    const data = loadJson(RETRY_FILE, {});
    const k = retryKey(filePath);
    data[k] = (data[k] || 0) + 1;
    fs.writeFileSync(RETRY_FILE, JSON.stringify(data, null, 2), 'utf8');
    return data[k];
  } catch { return 1; }
}

function resetRetry(filePath) {
  try {
    const data = loadJson(RETRY_FILE, {});
    delete data[retryKey(filePath)];
    fs.writeFileSync(RETRY_FILE, JSON.stringify(data, null, 2), 'utf8');
  } catch {}
}

function loadJson(p, fallback) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); }
  catch { return fallback; }
}

function recordLesson(summary) {
  try {
    const dir = path.dirname(LESSONS_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const date = new Date().toISOString().slice(0, 10);
    const entry = `## ${date}\n\n${truncate(summary, 1000)}\n\n`;
    let existing = '';
    if (safeExists(LESSONS_FILE)) existing = fs.readFileSync(LESSONS_FILE, 'utf8');
    fs.writeFileSync(LESSONS_FILE, entry + existing, 'utf8');
  } catch {}
}

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch { process.stdout.write('{}'); return; }
  if (data.stop_hook_active === true) { process.stdout.write('{}'); return; }

  const sessionId = data.session_id || '';
  const lastMsg = data.last_assistant_message || '';
  appendLog(sessionId, 'subagent_stop', {
    agent_id: data.agent_id,
    last_assistant_message_preview: lastMsg.slice(0, 200),
  });

  const changed = getChangedFiles();
  if (changed.length === 0) { process.stdout.write('{}'); return; }

  const pyFiles = changed.filter(f => f.endsWith('.py'));
  const tsFiles = changed.filter(f => f.endsWith('.ts') || f.endsWith('.tsx'));
  const jsFiles = changed.filter(f => f.endsWith('.js') || f.endsWith('.jsx'));

  const errors = [];
  if (pyFiles.length) {
    const r = runRuff(pyFiles); if (r) errors.push(r);
    const p = runPyright(pyFiles); if (p) errors.push(p);
  }
  if (tsFiles.length) {
    const t = runTsc(); if (t) errors.push(t);
  }
  if (jsFiles.length) {
    const e = runEslint(jsFiles); if (e) errors.push(e);
  }

  // Map related tests.
  const pyTests = [...new Set(pyFiles.flatMap(pythonTestsFor))];
  const tsTests = [...new Set(tsFiles.flatMap(tsTestsFor))];
  if (pyTests.length) { const r = runPytest(pyTests); if (r) errors.push(r); }
  if (tsTests.length) { const r = runVitest(tsTests); if (r) errors.push(r); }

  if (errors.length === 0) {
    for (const f of changed) resetRetry(f);
    process.stdout.write('{}');
    return;
  }

  const failedFiles = [...new Set([...pyFiles, ...tsFiles, ...jsFiles])];
  const summary = errors.join('\n\n');

  // Find the first file that's already degraded.
  const degraded = failedFiles.find(f => getRetry(f) >= MAX_RETRIES);
  if (degraded) {
    appendLog(sessionId, 'subagent_stop_degraded', { file: degraded, retries: MAX_RETRIES });
    process.stdout.write('{}'); // degrade: stop blocking
    return;
  }

  for (const f of failedFiles) bumpRetry(f);

  appendLog(sessionId, 'subagent_stop_failed', {
    files: failedFiles,
    errors: summary.slice(0, 500),
  });
  recordLesson(summary);

  process.stdout.write(JSON.stringify({
    decision: 'block',
    reason: `Quality checks failed for ${failedFiles.join(', ')}:\n${summary}. Fix and retry.`,
  }));
}

process.stdin.resume();

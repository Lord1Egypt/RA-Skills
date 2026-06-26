#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const DEFAULT_ENV = '/home/node/.openclaw/.env';
const DEFAULT_POLICY = '/home/node/.openclaw/envsafe-policy.json';
const KEY_RE = /^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=/;
const STRICT_KEY_RE = /^[A-Za-z_][A-Za-z0-9_]*$/;

function parseArgs(argv) {
  const out = {
    file: DEFAULT_ENV,
    policy: DEFAULT_POLICY,
    profile: '',
    backupKeep: 20,
    backupTtlDays: 7,
    lockTimeoutMs: 5000,
    lockStaleMs: 300000,
    dedupe: 'keep-last',
    requireStdin: true,
    allowArgv: false,
    auditLog: '/home/node/.openclaw/envsafe-audit.log',
    keyNamePattern: '^[A-Z][A-Z0-9_]*$',
    commentPattern: '.*used-by:.*updated:.*',
    requireCommentForNew: true,
    requireCommentInLint: false,
    protectedKeys: [],
    requiredProfiles: {},
    defaultProfile: '',
    strict: false,
    _: [],
    __explicit: new Set(),
  };

  function setOpt(k, v = true) {
    out[k] = v;
    out.__explicit.add(k);
  }

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--file') setOpt('file', argv[++i]);
    else if (a === '--policy') setOpt('policy', argv[++i]);
    else if (a === '--profile') setOpt('profile', argv[++i]);
    else if (a === '--stdin') setOpt('stdin', true);
    else if (a === '--allow-argv') setOpt('allowArgv', true);
    else if (a === '--if-missing') setOpt('ifMissing', true);
    else if (a === '--dry-run') setOpt('dryRun', true);
    else if (a === '--strict') setOpt('strict', true);
    else if (a === '--force') setOpt('force', true);
    else if (a === '--backup-keep') setOpt('backupKeep', Number(argv[++i]));
    else if (a === '--backup-ttl-days') setOpt('backupTtlDays', Number(argv[++i]));
    else if (a === '--lock-timeout-ms') setOpt('lockTimeoutMs', Number(argv[++i]));
    else if (a === '--lock-stale-ms') setOpt('lockStaleMs', Number(argv[++i]));
    else if (a === '--audit-log') setOpt('auditLog', argv[++i]);
    else if (a === '--comment') setOpt('comment', argv[++i]);
    else if (a === '--key-name-pattern') setOpt('keyNamePattern', argv[++i]);
    else if (a === '--comment-pattern') setOpt('commentPattern', argv[++i]);
    else if (a === '--require-comment-for-new') setOpt('requireCommentForNew', true);
    else if (a === '--no-require-comment-for-new') setOpt('requireCommentForNew', false);
    else if (a === '--require-comment-in-lint') setOpt('requireCommentInLint', true);
    else if (a === '--dedupe') setOpt('dedupe', argv[++i] || 'keep-last');
    else out._.push(a);
  }
  return out;
}

function die(msg, code = 2) {
  console.error(msg);
  process.exit(code);
}

function readJson(file) {
  if (!file || !fs.existsSync(file)) return null;
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    die(`invalid policy json: ${file}`);
  }
}

function applyPolicy(opts) {
  const raw = readJson(opts.policy);
  if (!raw) return;

  const d = raw.defaults || {};
  const mapDefaults = [
    'file',
    'backupKeep',
    'backupTtlDays',
    'lockTimeoutMs',
    'lockStaleMs',
    'dedupe',
    'requireStdin',
    'allowArgv',
    'auditLog',
    'keyNamePattern',
    'commentPattern',
    'requireCommentForNew',
    'requireCommentInLint',
    'strict',
    'defaultProfile',
  ];

  for (const k of mapDefaults) {
    if (!opts.__explicit.has(k) && Object.prototype.hasOwnProperty.call(d, k)) {
      opts[k] = d[k];
    }
  }

  if (!opts.__explicit.has('protectedKeys') && Array.isArray(raw.protectedKeys)) {
    opts.protectedKeys = raw.protectedKeys.filter((x) => typeof x === 'string');
  }
  if (!opts.__explicit.has('requiredProfiles') && raw.requiredProfiles && typeof raw.requiredProfiles === 'object') {
    opts.requiredProfiles = raw.requiredProfiles;
  }

  if (!opts.__explicit.has('profile') && opts.defaultProfile && !opts.profile) {
    opts.profile = opts.defaultProfile;
  }
}

function readLines(file) {
  if (!fs.existsSync(file)) return [];
  const txt = fs.readFileSync(file, 'utf8');
  const lines = txt.split(/(?<=\n)/);
  if (lines.length === 1 && lines[0] === '') return [];
  return lines;
}

function buildText(lines) {
  return lines.join('');
}

function writeFileAtomic(file, text) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.tmp.${Date.now()}.${process.pid}`;
  fs.writeFileSync(tmp, text, { encoding: 'utf8', mode: 0o600 });
  fs.renameSync(tmp, file);
  try {
    fs.chmodSync(file, 0o600);
  } catch (_) {}
}

function backupFile(file) {
  const now = new Date();
  const ts = now.toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
  const ms = String(now.getUTCMilliseconds()).padStart(3, '0');
  const bak = `${file}.bak.${ts}.${ms}.${process.pid}`;
  if (fs.existsSync(file)) {
    fs.copyFileSync(file, bak);
    try {
      fs.chmodSync(bak, 0o600);
    } catch (_) {}
  } else {
    fs.writeFileSync(bak, '', { encoding: 'utf8', mode: 0o600 });
  }
  return bak;
}

function pruneBackups(file, keep, ttlDays) {
  const dir = path.dirname(file);
  const base = path.basename(file);
  if (!fs.existsSync(dir)) return { deleted: 0, remaining: 0 };

  const now = Date.now();
  const ttlMs = Math.max(0, Number(ttlDays) || 0) * 24 * 60 * 60 * 1000;

  let backups = fs
    .readdirSync(dir)
    .filter((n) => n.startsWith(`${base}.bak.`))
    .map((n) => {
      const p = path.join(dir, n);
      const st = fs.statSync(p);
      return { path: p, mtimeMs: st.mtimeMs };
    })
    .sort((a, b) => b.mtimeMs - a.mtimeMs);

  let deleted = 0;

  if (ttlMs > 0) {
    for (const b of backups) {
      if (now - b.mtimeMs > ttlMs) {
        try {
          fs.unlinkSync(b.path);
          deleted++;
        } catch (_) {}
      }
    }
    backups = backups.filter((b) => fs.existsSync(b.path));
  }

  const keepN = Math.max(0, Number(keep) || 0);
  for (let i = keepN; i < backups.length; i++) {
    try {
      fs.unlinkSync(backups[i].path);
      deleted++;
    } catch (_) {}
  }

  const remaining = fs
    .readdirSync(dir)
    .filter((n) => n.startsWith(`${base}.bak.`)).length;
  return { deleted, remaining };
}

function extractKey(line) {
  const m = line.match(KEY_RE);
  return m ? m[1] : null;
}

function validateKey(key) {
  if (!STRICT_KEY_RE.test(key || '')) die(`invalid key: ${key}`);
}

function validateKeyByPolicy(opts, key) {
  validateKey(key);
  let re = null;
  try {
    re = new RegExp(opts.keyNamePattern || '^[A-Z][A-Z0-9_]*$');
  } catch (_) {
    die(`invalid keyNamePattern regex in policy: ${opts.keyNamePattern}`);
  }
  if (!re.test(key)) {
    die(`key does not match naming policy (${opts.keyNamePattern}): ${key}`);
  }
}

function listKeys(lines) {
  const out = [];
  for (const ln of lines) {
    const s = ln.trim();
    if (!s || s.startsWith('#')) continue;
    const k = extractKey(ln);
    if (k) out.push(k);
  }
  return out;
}

function normalizeValue(v) {
  if (v.includes('\n')) return JSON.stringify(v);
  return v;
}

function nowIso() {
  return new Date().toISOString();
}

function appendAudit(opts, event, fields = {}) {
  if (!opts.auditLog) return;
  try {
    fs.mkdirSync(path.dirname(opts.auditLog), { recursive: true });
    const line = JSON.stringify({ ts: nowIso(), event, file: opts.file, profile: opts.profile || null, ...fields }) + '\n';
    fs.appendFileSync(opts.auditLog, line, { encoding: 'utf8', mode: 0o600 });
    try { fs.chmodSync(opts.auditLog, 0o600); } catch (_) {}
  } catch (_) {
    // don't block main flow on audit failure
  }
}

function isProcessAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (_) {
    return false;
  }
}

function withLock(file, timeoutMs, staleMs, fn) {
  const lockFile = `${file}.lock`;
  const start = Date.now();

  while (true) {
    try {
      const fd = fs.openSync(lockFile, 'wx', 0o600);
      try {
        const payload = JSON.stringify({ pid: process.pid, ts: Date.now() });
        fs.writeFileSync(fd, payload);
      } catch (_) {}
      try {
        return fn();
      } finally {
        try {
          fs.closeSync(fd);
        } catch (_) {}
        try {
          fs.unlinkSync(lockFile);
        } catch (_) {}
      }
    } catch (_) {
      // stale-lock recovery (best effort)
      try {
        const st = fs.statSync(lockFile);
        if (Date.now() - st.mtimeMs > staleMs) {
          let stale = true;
          try {
            const raw = fs.readFileSync(lockFile, 'utf8');
            const obj = JSON.parse(raw);
            if (obj && Number.isInteger(obj.pid) && isProcessAlive(obj.pid)) stale = false;
          } catch (_) {}
          if (stale) fs.unlinkSync(lockFile);
        }
      } catch (_) {}

      if (Date.now() - start > timeoutMs) {
        die(`lock timeout after ${timeoutMs}ms: ${lockFile}`);
      }
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 100);
    }
  }
}

function lintFindings(file, opts = {}) {
  const lines = readLines(file);
  const seen = new Map();
  const invalidLines = [];
  const missingComments = [];
  let re = null;

  try {
    re = new RegExp(opts.keyNamePattern || '^[A-Z][A-Z0-9_]*$');
  } catch (_) {
    re = /^[A-Z][A-Z0-9_]*$/;
  }

  lines.forEach((ln, i) => {
    const n = i + 1;
    const s = ln.trim();
    if (!s || s.startsWith('#')) return;
    const k = extractKey(ln);
    if (!k) {
      invalidLines.push(n);
      return;
    }
    if (!seen.has(k)) seen.set(k, []);
    seen.get(k).push(n);

    if (!re.test(k)) {
      invalidLines.push(n);
    }

    if (opts.requireCommentInLint) {
      let hasComment = false;
      for (let j = i - 1; j >= 0; j--) {
        const prev = (lines[j] || '').trim();
        if (prev === '') continue;
        if (prev.startsWith('#')) {
          hasComment = true;
        }
        break;
      }
      if (!hasComment) missingComments.push({ key: k, line: n });
    }
  });

  const duplicates = [];
  for (const [k, locs] of seen.entries()) {
    if (locs.length > 1) duplicates.push({ key: k, lines: locs });
  }

  return {
    invalidLines,
    missingComments,
    duplicates,
    keyCount: seen.size,
    assignmentCount: [...seen.values()].reduce((a, x) => a + x.length, 0),
    keys: [...seen.keys()].sort(),
  };
}

function requiredMissing(opts, presentKeys) {
  const p = opts.profile;
  if (!p) return [];
  const req = opts.requiredProfiles?.[p];
  if (!Array.isArray(req)) return [];
  const set = new Set(presentKeys);
  return req.filter((k) => !set.has(k));
}

function cmdKeys(opts) {
  const keys = Array.from(new Set(listKeys(readLines(opts.file)))).sort();
  for (const k of keys) console.log(k);
}

function cmdExists(opts, key) {
  validateKeyByPolicy(opts, key);
  const keys = new Set(listKeys(readLines(opts.file)));
  console.log(keys.has(key) ? 'present' : 'missing');
}

function cmdLint(opts) {
  const f = lintFindings(opts.file, opts);
  for (const n of f.invalidLines) console.log(`line ${n}: invalid assignment syntax or key naming violation`);
  for (const d of f.duplicates) console.log(`duplicate key ${d.key} at lines ${d.lines.join(',')}`);
  for (const m of f.missingComments) console.log(`missing comment for key ${m.key} at line ${m.line}`);

  const missing = requiredMissing(opts, f.keys);
  if (missing.length) console.log(`missing_required(${opts.profile})=${missing.join(',')}`);

  if (f.invalidLines.length || f.duplicates.length || f.missingComments.length || missing.length) process.exit(2);
  console.log('OK');
}

function applySet(lines, key, value, dedupeMode, ifMissing, comment) {
  const newline = `${key}=${value}\n`;
  const idxs = [];
  for (let i = 0; i < lines.length; i++) {
    if (extractKey(lines[i]) === key) idxs.push(i);
  }

  const out = [...lines];
  let changed = 0;
  let removed = 0;
  let skipped = 0;

  if (idxs.length === 0) {
    if (out.length > 0 && !out[out.length - 1].endsWith('\n')) out[out.length - 1] += '\n';
    if (comment && comment.trim()) {
      const c = comment.trim().replace(/^#+\s*/, '');
      out.push(`# ${c}\n`);
    }
    out.push(newline);
    changed++;
    return { out, changed, removed, skipped };
  }

  if (ifMissing) {
    skipped = 1;
    return { out, changed, removed, skipped };
  }

  if (dedupeMode === 'none') {
    for (const i of idxs) {
      if (out[i] !== newline) {
        out[i] = newline;
        changed++;
      }
    }
    return { out, changed, removed, skipped };
  }

  const keepIndex = dedupeMode === 'keep-first' ? idxs[0] : idxs[idxs.length - 1];
  const removedSet = new Set(idxs.filter((i) => i !== keepIndex));
  const deduped = [];
  for (let i = 0; i < out.length; i++) {
    if (removedSet.has(i)) {
      removed++;
      continue;
    }
    deduped.push(out[i]);
  }

  let keyLine = -1;
  for (let i = 0; i < deduped.length; i++) {
    if (extractKey(deduped[i]) === key) {
      keyLine = i;
      break;
    }
  }
  if (keyLine >= 0 && deduped[keyLine] !== newline) {
    deduped[keyLine] = newline;
    changed++;
  }

  return { out: deduped, changed, removed, skipped };
}

function enforcePolicyFileSafety(opts) {
  if (!opts.policy || !fs.existsSync(opts.policy)) return;
  try {
    const st = fs.statSync(opts.policy);
    const mode = st.mode & 0o777;
    if ((mode & 0o022) !== 0) {
      die(`insecure policy permissions: ${opts.policy} mode=${mode.toString(8)} (must not be group/world writable)`);
    }
  } catch (e) {
    die(`cannot stat policy file: ${opts.policy}`);
  }
}

function cmdSet(opts, key, valueArg) {
  validateKeyByPolicy(opts, key);
  if (!['keep-last', 'keep-first', 'none'].includes(opts.dedupe)) {
    die(`invalid --dedupe value: ${opts.dedupe}`);
  }

  let value;
  if (opts.stdin) {
    value = fs.readFileSync(0, 'utf8');
    if (value.endsWith('\n')) value = value.slice(0, -1);
  } else {
    if (opts.requireStdin && !opts.force) {
      die('stdin is required by policy. Use --stdin (or --force to override).');
    }
    if (!opts.allowArgv) {
      die('argv value disabled for safety. Use --stdin (preferred) or add --allow-argv explicitly.');
    }
    value = valueArg;
  }

  if (value === undefined) die('set requires value: use --stdin or --allow-argv <VALUE>');
  value = normalizeValue(value);

  // Pre-check outside lock to avoid lock leak on hard-exit paths
  const preLines = readLines(opts.file);
  const preExists = new Set(listKeys(preLines)).has(key);
  if (!preExists && opts.requireCommentForNew && !(opts.comment && String(opts.comment).trim())) {
    die(`comment required for new key: ${key} (use --comment "..." or disable via policy)`);
  }
  if (!preExists && opts.requireCommentForNew) {
    validateCommentByPolicy(opts, String(opts.comment || ''));
  }

  return withLock(opts.file, opts.lockTimeoutMs, opts.lockStaleMs, () => {
    const lines = readLines(opts.file);
    const result = applySet(lines, key, value, opts.dedupe, !!opts.ifMissing, opts.comment);

    if (!opts.dryRun) {
      const bak = backupFile(opts.file);
      writeFileAtomic(opts.file, buildText(result.out));
      const pruned = pruneBackups(opts.file, opts.backupKeep, opts.backupTtlDays);
      console.log(`changed=${result.changed}`);
      console.log(`removed=${result.removed}`);
      console.log(`skipped=${result.skipped}`);
      console.log(`backup=${bak}`);
      console.log(`backups_deleted=${pruned.deleted}`);
      console.log(`backups_remaining=${pruned.remaining}`);
      appendAudit(opts, 'set', { key, changed: result.changed, removed: result.removed, skipped: result.skipped, dryRun: false });
      return;
    }

    console.log('dry_run=true');
    console.log(`changed=${result.changed}`);
    console.log(`removed=${result.removed}`);
    console.log(`skipped=${result.skipped}`);
    appendAudit(opts, 'set', { key, changed: result.changed, removed: result.removed, skipped: result.skipped, dryRun: true });
  });
}

function applyUnset(lines, key) {
  const out = [];
  let removed = 0;
  for (const ln of lines) {
    if (extractKey(ln) === key) {
      removed++;
      continue;
    }
    out.push(ln);
  }
  return { out, removed };
}

function cmdUnset(opts, key) {
  validateKeyByPolicy(opts, key);
  if (opts.protectedKeys.includes(key) && !opts.force) {
    die(`refusing to unset protected key: ${key} (use --force to override)`);
  }

  return withLock(opts.file, opts.lockTimeoutMs, opts.lockStaleMs, () => {
    const lines = readLines(opts.file);
    const result = applyUnset(lines, key);

    if (!opts.dryRun) {
      const bak = backupFile(opts.file);
      writeFileAtomic(opts.file, buildText(result.out));
      const pruned = pruneBackups(opts.file, opts.backupKeep, opts.backupTtlDays);
      console.log(`removed=${result.removed}`);
      console.log(`backup=${bak}`);
      console.log(`backups_deleted=${pruned.deleted}`);
      console.log(`backups_remaining=${pruned.remaining}`);
      appendAudit(opts, 'unset', { key, removed: result.removed, dryRun: false });
      return;
    }

    console.log('dry_run=true');
    console.log(`removed=${result.removed}`);
    appendAudit(opts, 'unset', { key, removed: result.removed, dryRun: true });
  });
}

function cmdDoctor(opts) {
  const exists = fs.existsSync(opts.file);
  const f = lintFindings(opts.file);
  const dir = path.dirname(opts.file);
  const base = path.basename(opts.file);
  const backupCount = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((n) => n.startsWith(`${base}.bak.`)).length
    : 0;
  const missing = requiredMissing(opts, f.keys);

  console.log(`file=${opts.file}`);
  console.log(`policy=${opts.policy}`);
  console.log(`profile=${opts.profile || 'none'}`);
  console.log(`exists=${exists ? 'yes' : 'no'}`);
  console.log(`keys=${f.keyCount}`);
  console.log(`assignments=${f.assignmentCount}`);
  console.log(`invalid_lines=${f.invalidLines.length}`);
  console.log(`duplicate_keys=${f.duplicates.length}`);
  console.log(`missing_required=${missing.length}`);
  console.log(`key_name_pattern=${opts.keyNamePattern}`);
  console.log(`comment_pattern=${opts.commentPattern}`);
  console.log(`require_comment_for_new=${opts.requireCommentForNew ? 'yes' : 'no'}`);
  console.log(`require_comment_in_lint=${opts.requireCommentInLint ? 'yes' : 'no'}`);
  console.log(`backups=${backupCount}`);
  if (f.invalidLines.length) console.log(`invalid_line_numbers=${f.invalidLines.join(',')}`);
  if (f.duplicates.length) console.log(`duplicate_key_names=${f.duplicates.map((x) => x.key).join(',')}`);
  if (missing.length) console.log(`missing_required_keys=${missing.join(',')}`);

  appendAudit(opts, 'doctor', {
    invalidLines: f.invalidLines.length,
    duplicateKeys: f.duplicates.length,
    missingComments: f.missingComments.length,
    missingRequired: missing.length,
    strict: !!opts.strict,
  });

  if (opts.strict && (f.invalidLines.length || f.duplicates.length || f.missingComments.length || missing.length)) {
    process.exit(2);
  }
}

function validateCommentByPolicy(opts, comment) {
  let re = null;
  try {
    re = new RegExp(opts.commentPattern || '.*');
  } catch (_) {
    die(`invalid commentPattern regex in policy: ${opts.commentPattern}`);
  }
  if (!re.test(comment || '')) {
    die(`comment does not match policy (${opts.commentPattern}). include required fields like used-by and updated`);
  }
}

function usage() {
  console.log('usage: envsafe.js [--policy PATH] [--file PATH] [--profile NAME] [--dry-run] [--strict] [--stdin] [--allow-argv] [--comment TEXT] [--if-missing] [--force] [--dedupe keep-last|keep-first|none] [--audit-log PATH] [--lock-stale-ms N] [--key-name-pattern REGEX] [--comment-pattern REGEX] [--require-comment-in-lint] <keys|exists|set|unset|lint|doctor|policy|help> ...');
}

function cmdPolicy(opts) {
  console.log(`policy=${opts.policy}`);
  console.log(`file=${opts.file}`);
  console.log(`require_stdin=${opts.requireStdin ? 'yes' : 'no'}`);
  console.log(`allow_argv=${opts.allowArgv ? 'yes' : 'no'}`);
  console.log(`dedupe=${opts.dedupe}`);
  console.log(`backup_keep=${opts.backupKeep}`);
  console.log(`backup_ttl_days=${opts.backupTtlDays}`);
  console.log(`lock_timeout_ms=${opts.lockTimeoutMs}`);
  console.log(`lock_stale_ms=${opts.lockStaleMs}`);
  console.log(`audit_log=${opts.auditLog || ''}`);
  console.log(`strict_default=${opts.strict ? 'yes' : 'no'}`);
  console.log(`key_name_pattern=${opts.keyNamePattern}`);
  console.log(`comment_pattern=${opts.commentPattern}`);
  console.log(`require_comment_for_new=${opts.requireCommentForNew ? 'yes' : 'no'}`);
  console.log(`require_comment_in_lint=${opts.requireCommentInLint ? 'yes' : 'no'}`);
  console.log(`profile=${opts.profile || 'none'}`);
  console.log(`protected_keys=${opts.protectedKeys.join(',')}`);
}

(function main() {
  const opts = parseArgs(process.argv.slice(2));
  applyPolicy(opts);
  enforcePolicyFileSafety(opts);
  const [cmd, a1, a2] = opts._;

  if (!cmd || cmd === 'help') {
    usage();
    return;
  }
  if (cmd === '--help' || cmd === '-h') {
    usage();
    return;
  }

  if (cmd === 'keys') return cmdKeys(opts);
  if (cmd === 'exists') return cmdExists(opts, a1);
  if (cmd === 'lint') return cmdLint(opts);
  if (cmd === 'doctor') return cmdDoctor(opts);
  if (cmd === 'policy') return cmdPolicy(opts);
  if (cmd === 'set') return cmdSet(opts, a1, a2);
  if (cmd === 'unset') return cmdUnset(opts, a1);

  die(`unknown command: ${cmd}`);
})();

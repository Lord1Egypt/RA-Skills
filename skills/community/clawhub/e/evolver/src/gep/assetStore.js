const fs = require('fs');
const path = require('path');
const { getGepAssetsDir, getBundledGepAssetsDir, getRepoRoot, getSessionScope } = require('./paths');
const { computeAssetId, SCHEMA_VERSION } = require('./contentHash');
const { validateGene } = require('./schemas/gene');
const { validateCapsule } = require('./schemas/capsule');

// Run validateGene/validateCapsule before persisting. Warn-only -- never throw
// because losing a write hurts more than persisting a slightly-malformed
// record. The hub has its own validation gate when the asset is published.
// See issue #30 (H1) for context.
function _validateAssetWarn(label, validatorFn, obj) {
  try {
    validatorFn(obj);
  } catch (e) {
    console.warn('[AssetStore] ' + label + ' schema validation warning: ' + (e && e.message || e));
  }
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// ---------------------------------------------------------------------------
// File-level advisory locking for JSON read-modify-write operations.
//
// Problem: multiple processes (daemon + CLI script + cron) can each call
// loadGenes() -> mutate -> writeJsonAtomic(), which is safe for a single
// writer but loses updates when two processes interleave their read/write
// windows. writeJsonAtomic is atomic w.r.t. partial writes, not w.r.t. the
// enclosing read-modify-write transaction.
//
// Solution: O_EXCL-based lock file next to the target. Each writer acquires
// the lock, runs its read/update/write, then releases. Stale locks (owner
// PID no longer alive) are detected and reclaimed to avoid deadlock after
// a crash.
//
// Synchronous by design -- all callers (upsertGene, appendCapsule, etc.) are
// synchronous and run on the main loop. We keep the retry loop cheap using a
// short busy-wait bounded by LOCK_TIMEOUT_MS, which is acceptable given lock
// contention is rare in practice (one daemon per machine).
// ---------------------------------------------------------------------------
const LOCK_TIMEOUT_MS = 5000;
const LOCK_RETRY_INTERVAL_MS = 20;

// Synchronous sleep that parks the main thread without burning CPU.
// Note: this still blocks the event loop (Atomics.wait is sync-blocking
// on the main thread) — heartbeat/ATP/proxy callbacks remain stalled
// during lock contention. The win here is CPU usage, not responsiveness.
// Pattern mirrors policyCheck.sleepSync (src/gep/policyCheck.js:435-443).
function _busyWait(ms) {
  const t = Math.max(0, ms);
  try {
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, t);
  } catch (_) {
    const end = Date.now() + t;
    while (Date.now() < end) { /* busy wait fallback */ }
  }
}

function _acquireLock(targetPath) {
  const lockPath = targetPath + '.lock';
  const deadline = Date.now() + LOCK_TIMEOUT_MS;
  while (Date.now() < deadline) {
    try {
      fs.writeFileSync(lockPath, String(process.pid), { flag: 'wx', encoding: 'utf8' });
      return lockPath;
    } catch (e) {
      if (e && e.code !== 'EEXIST') throw e;
      try {
        const pidStr = fs.readFileSync(lockPath, 'utf8').trim();
        const ownerPid = parseInt(pidStr, 10);
        if (Number.isFinite(ownerPid) && ownerPid > 0 && ownerPid !== process.pid) {
          try {
            process.kill(ownerPid, 0);
          } catch (_ownerErr) {
            try { fs.unlinkSync(lockPath); } catch (_e2) {}
            continue;
          }
        }
      } catch (_readErr) {}
      _busyWait(LOCK_RETRY_INTERVAL_MS);
    }
  }
  throw new Error('[AssetStore] Lock timeout (' + LOCK_TIMEOUT_MS + 'ms) for: ' + targetPath);
}

function _releaseLock(lockPath) {
  if (!lockPath) return;
  try { fs.unlinkSync(lockPath); } catch (_) {}
}

function withFileLock(targetPath, fn) {
  const lockPath = _acquireLock(targetPath);
  try {
    return fn();
  } finally {
    _releaseLock(lockPath);
  }
}

function readJsonIfExists(filePath, fallback) {
  try {
    if (!fs.existsSync(filePath)) return fallback;
    const raw = fs.readFileSync(filePath, 'utf8');
    if (!raw.trim()) return fallback;
    return JSON.parse(raw);
  } catch (e) {
    console.warn('[AssetStore] Failed to read ' + filePath + ':', e && e.message || e);
    return fallback;
  }
}

function writeJsonAtomic(filePath, obj) {
  const dir = path.dirname(filePath);
  ensureDir(dir);
  const tmp = `${filePath}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(obj, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, filePath);
}

// Build a validation command using repo-root-relative paths.
// runValidations() executes with cwd=repoRoot, so require('./src/...')
// resolves correctly without embedding machine-specific absolute paths.
function buildValidationCmd(relModules) {
  const paths = relModules.map(m => `./${m}`);
  return `node scripts/validate-modules.js ${paths.join(' ')}`;
}

function getDefaultGenes() {
  return {
    version: 1,
    genes: [
      {
        type: 'Gene', id: 'gene_gep_repair_from_errors', category: 'repair',
        signals_match: [
          'error|错误|异常|エラー|오류',
          'exception|异常|例外|예외',
          'failed|失败|失敗|실패|fail',
          'unstable|不稳定|不安定|불안정',
          'log_error',
          'test_failure',
        ],
        preconditions: ['signals contains error-related indicators'],
        strategy: [
          'Extract structured signals from logs and user instructions',
          'Select an existing Gene by signals match (no improvisation)',
          'Estimate blast radius (files, lines) before editing',
          'Apply smallest reversible patch',
          'Validate using declared validation steps; rollback on failure',
          'Solidify knowledge: append EvolutionEvent, update Gene/Capsule store',
        ],
        constraints: { max_files: 12, forbidden_paths: ['.git', 'node_modules'] },
        validation: [
          buildValidationCmd(['src/evolve', 'src/gep/solidify', 'src/gep/policyCheck', 'src/gep/selector', 'src/gep/memoryGraph', 'src/gep/assetStore']),
          'node scripts/validate-suite.js',
        ],
      },
      {
        type: 'Gene', id: 'gene_gep_optimize_prompt_and_assets', category: 'optimize',
        signals_match: [
          'protocol|协议|プロトコル|프로토콜',
          'gep',
          'prompt|提示词|提示|プロンプト|프롬프트',
          'audit|审计|監査|감사',
          'reusable|可复用|再利用|재사용',
        ],
        preconditions: ['need stricter, auditable evolution protocol outputs'],
        strategy: [
          'Extract signals and determine selection rationale via Selector JSON',
          'Prefer reusing existing Gene/Capsule; only create if no match exists',
          'Refactor prompt assembly to embed assets (genes, capsules, parent event)',
          'Reduce noise and ambiguity; enforce strict output schema',
          'Validate by running node index.js run and ensuring no runtime errors',
          'Solidify: record EvolutionEvent, update Gene definitions, create Capsule on success',
        ],
        constraints: { max_files: 20, forbidden_paths: ['.git', 'node_modules'] },
        validation: [
          buildValidationCmd(['src/evolve', 'src/gep/prompt', 'src/gep/contentHash', 'src/gep/skillDistiller']),
          'node scripts/validate-suite.js',
        ],
      },
      {
        type: 'Gene', id: 'gene_tool_integrity', category: 'repair',
        signals_match: ['tool_bypass|工具绕过|ツール迂回|도구우회'],
        preconditions: ['agent used shell/exec to perform an action that a registered tool can handle'],
        strategy: [
          'Always prefer registered tools over ad-hoc scripts or shell workarounds',
          'If a registered tool fails, report the actual error honestly and attempt to fix the root cause',
          'Never fabricate explanations -- describe actual actions transparently',
          'Do not create temporary scripts in extension or project directories',
        ],
        constraints: { max_files: 4, forbidden_paths: ['.git', 'node_modules'] },
        validation: [
          'node scripts/validate-suite.js',
        ],
        anti_patterns: ['tool_bypass'],
        routing_hint: { tier: 'cheap', reasoning_level: 'low' },
      },
    ],
  };
}

function getDefaultCapsules() { return { version: 1, capsules: [] }; }
function genesPath() { return path.join(getGepAssetsDir(), 'genes.json'); }
function genesSeedPath() { return path.join(getBundledGepAssetsDir(), 'genes.seed.json'); }
function bundledGenesPath() { return path.join(getBundledGepAssetsDir(), 'genes.json'); }
function capsulesPath() { return path.join(getGepAssetsDir(), 'capsules.json'); }
function capsulesJsonlPath() { return path.join(getGepAssetsDir(), 'capsules.jsonl'); }
function eventsPath() { return path.join(getGepAssetsDir(), 'events.jsonl'); }
function candidatesPath() { return path.join(getGepAssetsDir(), 'candidates.jsonl'); }
function externalCandidatesPath() { return path.join(getGepAssetsDir(), 'external_candidates.jsonl'); }
function failedCapsulesPath() { return path.join(getGepAssetsDir(), 'failed_capsules.json'); }
function pendingSignalsPath() { return path.join(getGepAssetsDir(), 'pending_signals.json'); }

// Explicit signal injection channel. A user (or an external tool) can declare
// arbitrary signals out-of-band by writing
//   { "signals": ["publish_markdown_to_feishu", ...], "note": "..." }
// to <gep-assets-dir>/pending_signals.json (getGepAssetsDir(), default
// .evolver/gep -- see #166). The signal-extraction stage reads these
// once and injects them into the cycle's signal set, bypassing the closed
// OPPORTUNITY_SIGNALS vocabulary that regex/keyword/LLM extraction is limited
// to. This is how a human-verified, deterministic capability (whose intent no
// extractor would ever map to a first-class signal) gets a chance to select
// its dedicated Gene.
//
// Read-once semantics: the file is consumed (emptied to {signals:[]}) under a
// file lock so the same explicit intent does not re-fire on every subsequent
// cycle. Returns the array of signal strings that were pending (possibly []).
function consumePendingSignals() {
  const p = pendingSignalsPath();
  if (!fs.existsSync(p)) return [];
  return withFileLock(p, () => {
    const data = readJsonIfExists(p, { signals: [] });
    const raw = data && Array.isArray(data.signals) ? data.signals : [];
    const signals = raw
      .map(s => (typeof s === 'string' ? s.trim() : ''))
      .filter(s => s.length > 0 && s.length <= 200);
    // Consume whenever the file held any entries -- even if every entry was
    // blank / over-length / non-string and none survived filtering. Otherwise
    // a file like {signals:["  "]} is re-read (under lock) on every later
    // cycle and read-once never completes. raw.length===0 means nothing to
    // consume (no pending signals, an already-emptied file, or a malformed
    // file that readJsonIfExists already warned about); skip the write to
    // avoid needless churn and to preserve a corrupt file for the user to fix.
    if (raw.length > 0) {
      // Consume: leave an empty, well-formed file so the next cycle is a no-op.
      writeJsonAtomic(p, { signals: [], note: '' });
    }
    return signals;
  });
}

const LEGACY_RUNTIME_FILENAMES = [
  'genes.json',
  'capsules.json',
  'genes.jsonl',
  'capsules.jsonl',
  'events.jsonl',
  'candidates.jsonl',
  'external_candidates.jsonl',
  'failed_capsules.json',
];

function legacyGepAssetsDir() {
  const baseDir = path.join(getRepoRoot(), 'assets', 'gep');
  const scope = getSessionScope();
  if (scope) {
    return path.join(baseDir, 'scopes', scope);
  }
  return baseDir;
}

function migrateLegacyRuntimeAssets() {
  if (process.env.GEP_ASSETS_DIR) return;
  const targetDir = getGepAssetsDir();
  const legacyDir = legacyGepAssetsDir();
  if (path.resolve(targetDir) === path.resolve(legacyDir)) return;
  if (!fs.existsSync(legacyDir)) return;

  let copied = 0;
  for (const name of LEGACY_RUNTIME_FILENAMES) {
    const from = path.join(legacyDir, name);
    const to = path.join(targetDir, name);
    try {
      if (!fs.existsSync(from) || fs.existsSync(to)) continue;
      ensureDir(path.dirname(to));
      fs.copyFileSync(from, to);
      copied++;
    } catch (e) {
      console.warn('[AssetStore] Failed to migrate legacy GEP asset ' + from + ':', e && e.message || e);
    }
  }
  if (copied > 0) {
    console.log('[AssetStore] Migrated ' + copied + ' GEP asset file(s) from ' + legacyDir + ' to ' + targetDir);
  }
}

// First-run seeding: if the user has no local genes.json yet, copy the
// shipped genes.seed.json into place so they start with the curated
// starter genes. Once genes.json exists, it is owned by the user and the
// seed is never re-applied -- this is what keeps `npm i -g @evomap/evolver`
// upgrades from wiping the user's accumulated asset store. See the
// 2026-05-03 regression report from Ruan Chengtao.
function ensureGenesSeeded() {
  migrateLegacyRuntimeAssets();
  const target = genesPath();
  if (fs.existsSync(target)) return;
  const seed = fs.existsSync(genesSeedPath()) ? genesSeedPath() : bundledGenesPath();
  if (!fs.existsSync(seed)) return;
  try {
    ensureDir(path.dirname(target));
    fs.copyFileSync(seed, target);
    console.log('[AssetStore] Seeded ' + target + ' from ' + path.basename(seed));
  } catch (e) {
    console.warn('[AssetStore] Failed to seed genes.json from seed:', e && e.message || e);
  }
}

function loadGenes() {
  ensureGenesSeeded();
  const jsonGenes = readJsonIfExists(genesPath(), getDefaultGenes()).genes || [];
  const jsonlGenes = [];
  try {
    const p = path.join(getGepAssetsDir(), 'genes.jsonl');
    if (fs.existsSync(p)) {
      const raw = fs.readFileSync(p, 'utf8');
      raw.split('\n').forEach(line => {
        if (line.trim()) {
          try {
            const parsed = JSON.parse(line);
            if (parsed && parsed.type === 'Gene') jsonlGenes.push(parsed);
          } catch(e) {}
        }
      });
    }
  } catch(e) {
    console.warn('[AssetStore] Failed to read genes.jsonl:', e && e.message || e);
  }

  // Combine and deduplicate by ID (JSONL takes precedence). Do NOT pass loaded
  // genes through createGene() — that would synthesize default fields
  // (epigenetic_marks, learning_history, anti_patterns, summary,
  // schema_version) on legacy genes that pre-date those fields, which would
  // change their content hash and invalidate any previously-computed
  // asset_id. Read paths must preserve on-disk gene shapes byte-for-byte;
  // callers that need normalized fields should call createGene() explicitly
  // (and write back via upsertGene which recomputes asset_id).
  const combined = [...jsonGenes, ...jsonlGenes];
  const unique = new Map();
  combined.forEach(g => {
    if (g && g.id) unique.set(String(g.id), g);
  });
  return Array.from(unique.values());
}

function loadCapsules() {
  const legacy = readJsonIfExists(capsulesPath(), getDefaultCapsules()).capsules || [];
  const jsonlCapsules = [];
  try {
    const p = capsulesJsonlPath();
    if (fs.existsSync(p)) {
      const raw = fs.readFileSync(p, 'utf8');
      raw.split('\n').forEach(line => {
        if (line.trim()) {
            try { jsonlCapsules.push(JSON.parse(line)); } catch(e) {}
        }
      });
    }
  } catch(e) {
    console.warn('[AssetStore] Failed to read capsules.jsonl:', e && e.message || e);
  }
  
  // Combine and deduplicate by ID
  const combined = [...legacy, ...jsonlCapsules];
  const unique = new Map();
  combined.forEach(c => {
      if (c && c.id) unique.set(String(c.id), c);
  });
  return Array.from(unique.values());
}

// Grow the tail chunk until it strictly contains the final newline-terminated
// line, then JSON.parse it. A single event embeds the full ValidationReport
// (up to ~4000 chars stdout + ~4000 chars stderr per command, plus blast
// radius / metadata), so individual lines routinely exceed 4 KB and can reach
// tens of KB. A fixed small chunk would either capture only the truncated
// tail of that JSON line (parse error -> null -> broken parent/child event
// chain) or still straddle the line boundary. Bugbot caught this on PR #34.
const LAST_EVENT_INITIAL_CHUNK = 64 * 1024;
const LAST_EVENT_MAX_CHUNK = 4 * 1024 * 1024;

function getLastEventId() {
  try {
    const p = eventsPath();
    if (!fs.existsSync(p)) return null;
    const stat = fs.statSync(p);
    if (stat.size === 0) return null;

    const cap = Math.min(stat.size, LAST_EVENT_MAX_CHUNK);
    let chunkSize = Math.min(stat.size, LAST_EVENT_INITIAL_CHUNK);

    const fd = fs.openSync(p, 'r');
    try {
      while (true) {
        const buf = Buffer.alloc(chunkSize);
        const readPos = stat.size - chunkSize;
        fs.readSync(fd, buf, 0, chunkSize, readPos);

        // Drop the trailing newline(s) the writer appends so lastIndexOf('\n')
        // points to the boundary BEFORE the final line, not at end-of-file.
        const trimmedTail = buf.toString('utf8').replace(/\n+$/, '');
        const lastNl = trimmedTail.lastIndexOf('\n');

        // The chunk fully contains the last line when either we read from the
        // start of the file, or we found a newline that bounds the line on
        // the left. Otherwise the final line is bigger than the current chunk
        // and we must grow.
        if (readPos > 0 && lastNl < 0) {
          if (chunkSize < cap) {
            chunkSize = Math.min(cap, chunkSize * 2);
            continue;
          }
          return null;
        }

        const lastLine = (lastNl >= 0 ? trimmedTail.slice(lastNl + 1) : trimmedTail).trim();
        if (!lastLine) return null;

        let last;
        try {
          last = JSON.parse(lastLine);
        } catch (parseErr) {
          if (chunkSize < cap) {
            chunkSize = Math.min(cap, chunkSize * 2);
            continue;
          }
          throw parseErr;
        }
        return last && typeof last.id === 'string' ? last.id : null;
      }
    } finally {
      fs.closeSync(fd);
    }
  } catch (e) {
    console.warn('[AssetStore] Failed to read last event ID:', e && e.message || e);
    return null;
  }
}

// Soft cap on how much of events.jsonl we materialize into memory in one read.
// On long-running daemons the file accumulates thousands of large JSON objects
// (validation reports, blast radius, etc) and the previous full-read could
// allocate dozens of MB per call -- and computeCapsuleSuccessStreak invokes
// this on every successful solidify. Above the threshold we tail-read a chunk
// from EOF and discard the partial leading line, mirroring readRecentCandidates.
// All current callers only look at the recent window
// (signals.js -> slice(-80), guards.js -> slice(-threshold),
//  a2a.computeCapsuleSuccessStreak -> backwards scan), so dropping older
// records is acceptable for correctness. Tunable via EVOLVER_EVENTS_FULL_READ_MAX_BYTES.
const EVENTS_FULL_READ_MAX_BYTES_DEFAULT = 2 * 1024 * 1024;
const EVENTS_TAIL_READ_BYTES_DEFAULT = 2 * 1024 * 1024;

function _eventsFullReadMaxBytes() {
  const v = parseInt(String(process.env.EVOLVER_EVENTS_FULL_READ_MAX_BYTES || ''), 10);
  return Number.isFinite(v) && v > 0 ? v : EVENTS_FULL_READ_MAX_BYTES_DEFAULT;
}

function _eventsTailReadBytes() {
  const v = parseInt(String(process.env.EVOLVER_EVENTS_TAIL_READ_BYTES || ''), 10);
  return Number.isFinite(v) && v > 0 ? v : EVENTS_TAIL_READ_BYTES_DEFAULT;
}

function readAllEvents() {
  try {
    const p = eventsPath();
    if (!fs.existsSync(p)) return [];
    const stat = fs.statSync(p);
    const fullReadCap = _eventsFullReadMaxBytes();
    if (stat.size <= fullReadCap) {
      const raw = fs.readFileSync(p, 'utf8');
      return raw.split('\n').map(l => l.trim()).filter(Boolean).map(l => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);
    }
    // Large file: tail-read to avoid OOM. Drop the first line ONLY when the
    // chunk does not cover the whole file (readPos > 0), because in that case
    // it can be cut mid-JSON. When chunkSize === stat.size the read starts at
    // 0 and the first line is the actual start-of-file -- discarding it would
    // silently lose a complete event. Bugbot caught this on PR #31.
    const chunkSize = Math.min(stat.size, _eventsTailReadBytes());
    const readPos = stat.size - chunkSize;
    const fd = fs.openSync(p, 'r');
    try {
      const buf = Buffer.alloc(chunkSize);
      fs.readSync(fd, buf, 0, chunkSize, readPos);
      const lines = buf.toString('utf8').split('\n').map(l => l.trim()).filter(Boolean);
      const intact = readPos > 0 && lines.length > 1 ? lines.slice(1) : lines;
      return intact.map(l => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);
    } finally {
      fs.closeSync(fd);
    }
  } catch (e) {
    console.warn('[AssetStore] Failed to read events.jsonl:', e && e.message || e);
    return [];
  }
}

function appendEventJsonl(eventObj) {
  const dir = getGepAssetsDir(); ensureDir(dir);
  fs.appendFileSync(eventsPath(), JSON.stringify(eventObj) + '\n', 'utf8');
}

function appendCandidateJsonl(candidateObj) {
  const dir = getGepAssetsDir(); ensureDir(dir);
  fs.appendFileSync(candidatesPath(), JSON.stringify(candidateObj) + '\n', 'utf8');
}

function appendExternalCandidateJsonl(obj) {
  const dir = getGepAssetsDir(); ensureDir(dir);
  fs.appendFileSync(externalCandidatesPath(), JSON.stringify(obj) + '\n', 'utf8');
}

function readRecentCandidates(limit = 20) {
  try {
    const p = candidatesPath();
    if (!fs.existsSync(p)) return [];
    const stat = fs.statSync(p);
    if (stat.size < 1024 * 1024) {
      const raw = fs.readFileSync(p, 'utf8');
      const lines = raw.split('\n').map(l => l.trim()).filter(Boolean);
      return lines.slice(-limit).map(l => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);
    }
    // Large file (>1MB): only read the tail to avoid OOM.
    const fd = fs.openSync(p, 'r');
    try {
      const chunkSize = Math.min(stat.size, limit * 4096);
      const buf = Buffer.alloc(chunkSize);
      fs.readSync(fd, buf, 0, chunkSize, stat.size - chunkSize);
      const lines = buf.toString('utf8').split('\n').map(l => l.trim()).filter(Boolean);
      return lines.slice(-limit).map(l => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);
    } finally {
      fs.closeSync(fd);
    }
  } catch (e) {
    console.warn('[AssetStore] Failed to read candidates.jsonl:', e && e.message || e);
    return [];
  }
}

function readRecentExternalCandidates(limit = 50) {
  try {
    const p = externalCandidatesPath();
    if (!fs.existsSync(p)) return [];
    const stat = fs.statSync(p);
    if (stat.size < 1024 * 1024) {
      const raw = fs.readFileSync(p, 'utf8');
      const lines = raw.split('\n').map(l => l.trim()).filter(Boolean);
      return lines.slice(-limit).map(l => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);
    }
    const fd = fs.openSync(p, 'r');
    try {
      const chunkSize = Math.min(stat.size, limit * 4096);
      const buf = Buffer.alloc(chunkSize);
      fs.readSync(fd, buf, 0, chunkSize, stat.size - chunkSize);
      const lines = buf.toString('utf8').split('\n').map(l => l.trim()).filter(Boolean);
      return lines.slice(-limit).map(l => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);
    } finally {
      fs.closeSync(fd);
    }
  } catch (e) {
    console.warn('[AssetStore] Failed to read external_candidates.jsonl:', e && e.message || e);
    return [];
  }
}

// Safety net: ensure schema_version and asset_id are present before writing.
function ensureSchemaFields(obj) {
  if (!obj || typeof obj !== 'object') return obj;
  if (!obj.schema_version) obj.schema_version = SCHEMA_VERSION;
  if (!obj.asset_id) {
    try { obj.asset_id = computeAssetId(obj); } catch (e) {
      console.warn('[AssetStore] Failed to compute asset ID:', e && e.message || e);
    }
  }
  return obj;
}

// Recompute asset_id from current content. Called on the Gene write path
// because solidify mutates epigenetic_marks / learning_history in place
// (see src/gep/solidify.js applyEpigeneticMarks + adaptGeneFromLearning),
// which would otherwise leave a stale content hash on disk -- breaking
// content addressing, dedup, and any tamper check that re-verifies
// asset_id against the persisted Gene. See issue #103.
function recomputeAssetId(obj) {
  if (!obj || typeof obj !== 'object') return obj;
  try {
    obj.asset_id = computeAssetId(obj);
  } catch (e) {
    console.warn('[AssetStore] Failed to recompute asset ID:', e && e.message || e);
  }
  return obj;
}

function upsertGene(geneObj) {
  _validateAssetWarn('Gene', validateGene, geneObj);
  ensureSchemaFields(geneObj);
  recomputeAssetId(geneObj);
  ensureGenesSeeded();
  return withFileLock(genesPath(), () => {
    const current = readJsonIfExists(genesPath(), getDefaultGenes());
    const genes = Array.isArray(current.genes) ? current.genes : [];
    const idx = genes.findIndex(g => g && g.id === geneObj.id);
    if (idx >= 0) genes[idx] = geneObj; else genes.push(geneObj);
    writeJsonAtomic(genesPath(), { version: current.version || 1, genes });
  });
}

function appendCapsule(capsuleObj) {
  _validateAssetWarn('Capsule', validateCapsule, capsuleObj);
  ensureSchemaFields(capsuleObj);
  return withFileLock(capsulesPath(), () => {
    const current = readJsonIfExists(capsulesPath(), getDefaultCapsules());
    const capsules = Array.isArray(current.capsules) ? current.capsules : [];
    capsules.push(capsuleObj);
    writeJsonAtomic(capsulesPath(), { version: current.version || 1, capsules });
  });
}

function upsertCapsule(capsuleObj) {
  if (!capsuleObj || capsuleObj.type !== 'Capsule' || !capsuleObj.id) return;
  _validateAssetWarn('Capsule', validateCapsule, capsuleObj);
  ensureSchemaFields(capsuleObj);
  return withFileLock(capsulesPath(), () => {
    const current = readJsonIfExists(capsulesPath(), getDefaultCapsules());
    const capsules = Array.isArray(current.capsules) ? current.capsules : [];
    const idx = capsules.findIndex(c => c && c.type === 'Capsule' && String(c.id) === String(capsuleObj.id));
    if (idx >= 0) capsules[idx] = capsuleObj; else capsules.push(capsuleObj);
    writeJsonAtomic(capsulesPath(), { version: current.version || 1, capsules });
  });
}

const FAILED_CAPSULES_MAX = 200;
const FAILED_CAPSULES_TRIM_TO = 100;

function getDefaultFailedCapsules() { return { version: 1, failed_capsules: [] }; }

function appendFailedCapsule(capsuleObj) {
  if (!capsuleObj || typeof capsuleObj !== 'object') return;
  ensureSchemaFields(capsuleObj);
  return withFileLock(failedCapsulesPath(), () => {
    const current = readJsonIfExists(failedCapsulesPath(), getDefaultFailedCapsules());
    let list = Array.isArray(current.failed_capsules) ? current.failed_capsules : [];
    list.push(capsuleObj);
    if (list.length > FAILED_CAPSULES_MAX) {
      list = list.slice(list.length - FAILED_CAPSULES_TRIM_TO);
    }
    writeJsonAtomic(failedCapsulesPath(), { version: current.version || 1, failed_capsules: list });
  });
}

function readRecentFailedCapsules(limit) {
  const n = Number.isFinite(Number(limit)) && Number(limit) > 0 ? Number(limit) : 50;
  try {
    const current = readJsonIfExists(failedCapsulesPath(), getDefaultFailedCapsules());
    const list = Array.isArray(current.failed_capsules) ? current.failed_capsules : [];
    return list.slice(Math.max(0, list.length - n));
  } catch (e) {
    console.warn('[AssetStore] Failed to read failed_capsules.json:', e && e.message || e);
    return [];
  }
}

// Ensure all expected asset files exist on startup.
// Creates empty files for optional append-only stores so that
// external grep/read commands never fail with "No such file or directory".
function ensureAssetFiles() {
  const dir = getGepAssetsDir();
  ensureDir(dir);
  ensureGenesSeeded();
  const files = [
    { path: genesPath(), defaultContent: JSON.stringify(getDefaultGenes(), null, 2) + '\n' },
    { path: capsulesPath(), defaultContent: JSON.stringify(getDefaultCapsules(), null, 2) + '\n' },
    { path: path.join(dir, 'genes.jsonl'), defaultContent: '' },
    { path: eventsPath(), defaultContent: '' },
    { path: candidatesPath(), defaultContent: '' },
    { path: failedCapsulesPath(), defaultContent: JSON.stringify(getDefaultFailedCapsules(), null, 2) + '\n' },
  ];
  for (const f of files) {
    if (!fs.existsSync(f.path)) {
      try {
        fs.writeFileSync(f.path, f.defaultContent, 'utf8');
      } catch (e) {
        // Non-fatal: log but continue
        console.error(`[AssetStore] Failed to create ${f.path}: ${e.message}`);
      }
    }
  }
}

module.exports = {
  loadGenes, loadCapsules, readAllEvents, getLastEventId,
  appendEventJsonl, appendCandidateJsonl, appendExternalCandidateJsonl,
  readRecentCandidates, readRecentExternalCandidates,
  upsertGene, appendCapsule, upsertCapsule,
  appendFailedCapsule, readRecentFailedCapsules,
  genesPath, capsulesPath, eventsPath, candidatesPath, externalCandidatesPath, failedCapsulesPath,
  pendingSignalsPath, consumePendingSignals,
  genesSeedPath, bundledGenesPath, ensureGenesSeeded, migrateLegacyRuntimeAssets,
  ensureAssetFiles, buildValidationCmd,
  withFileLock,
  readJsonIfExists,
};

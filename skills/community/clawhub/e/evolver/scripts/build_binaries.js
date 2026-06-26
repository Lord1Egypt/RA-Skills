#!/usr/bin/env node
/* eslint-disable no-console */
//
// build_binaries.js — produce standalone CLI binaries of evolver via the
// hardened "obfuscator -> bun bundle -> bun compile" pipeline.
//
// Pipeline (decided after empirical testing — see notes at end of this file):
//
//   1. bun build ./index.js --target=node --outfile=stage/bundled.js
//        -> resolves all require() into one self-contained file.
//
//   2. javascript-obfuscator stage/bundled.js -> stage/bundled.obf.js
//        -> high-strength config: stringArray (rc4) + controlFlowFlattening +
//           deadCodeInjection + identifier hex + splitStrings + numbers-to-expr.
//        -> selfDefending MUST be off: it triggers infinite-loop self-defense
//           when bun later wraps the bundle inside its standalone container.
//        -> renameGlobals MUST be off (otherwise bun's bundle step fails to
//           resolve dynamic require strings — but we already pass a single-file
//           bundle here, so this no longer applies; kept off for safety).
//        -> transformObjectKeys MUST be off (similar reason as above).
//
//   3. bun build stage/bundled.obf.js --compile --minify --target=<TARGET>
//        -> embeds bun runtime + bundled+obfuscated JS into a single executable.
//        -> --minify gives a second-pass identifier/whitespace squash on top
//           of the obfuscator output.
//
// Targets shipped (decision per AGENTS sync 2026-05-05):
//   bun-darwin-arm64  -> evolver-darwin-arm64
//   bun-darwin-x64    -> evolver-darwin-x64
//   bun-linux-x64     -> evolver-linux-x64
//   bun-linux-arm64   -> evolver-linux-arm64
//   bun-windows-x64   -> evolver-windows-x64.exe
//
// Usage:
//   node scripts/build_binaries.js              # builds all 4 targets
//   node scripts/build_binaries.js --target=darwin-arm64
//   node scripts/build_binaries.js --skip-obfuscate    # bun-only fast path (DEV)
//   node scripts/build_binaries.js --out-dir=dist-binaries
//   node scripts/build_binaries.js --dry-run
//
// Outputs:
//   <outDir>/evolver-<platform>           binary
//   <outDir>/evolver-<platform>.sha256    hash file (one line)
//   <outDir>/SHA256SUMS.txt               combined sha256 manifest
//
// Exit codes:
//   0  success
//   1  precondition failed (missing tool, version mismatch)
//   2  build step failed
//   3  smoke test of produced binary failed

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync, spawnSync } = require('child_process');

// ---------- argv ----------

const argv = process.argv.slice(2);
const OPTS = {
  target: null,
  skipObfuscate: false,
  outDir: 'dist-binaries',
  dryRun: false,
  keepStage: false,
};

for (const a of argv) {
  if (a === '--skip-obfuscate') OPTS.skipObfuscate = true;
  else if (a === '--dry-run') OPTS.dryRun = true;
  else if (a === '--keep-stage') OPTS.keepStage = true;
  else if (a.startsWith('--target=')) OPTS.target = a.slice('--target='.length);
  else if (a.startsWith('--out-dir=')) OPTS.outDir = a.slice('--out-dir='.length);
  else if (a === '--help' || a === '-h') {
    console.log(fs.readFileSync(__filename, 'utf8').split('\n').filter(l => l.startsWith('//')).map(l => l.replace(/^\/\/ ?/, '')).slice(0, 50).join('\n'));
    process.exit(0);
  } else {
    console.error(`build_binaries: unknown argument: ${a}`);
    process.exit(1);
  }
}

// ---------- constants ----------

const REPO_ROOT = path.resolve(__dirname, '..');
const ENTRY = path.join(REPO_ROOT, 'index.js');
const STAGE_DIR = path.join(REPO_ROOT, '.binary-stage');
const OUT_DIR = path.resolve(REPO_ROOT, OPTS.outDir);

const ALL_TARGETS = [
  { triple: 'bun-darwin-arm64',  name: 'evolver-darwin-arm64'  },
  { triple: 'bun-darwin-x64',    name: 'evolver-darwin-x64'    },
  { triple: 'bun-linux-x64',     name: 'evolver-linux-x64'     },
  { triple: 'bun-linux-arm64',   name: 'evolver-linux-arm64'   },
  { triple: 'bun-windows-x64',   name: 'evolver-windows-x64.exe' },
];

const TARGETS = OPTS.target
  ? ALL_TARGETS.filter(t => t.name.endsWith(OPTS.target) || t.triple.endsWith(OPTS.target))
  : ALL_TARGETS;

if (TARGETS.length === 0) {
  console.error(`build_binaries: target "${OPTS.target}" matched no known triple. Known: ${ALL_TARGETS.map(t => t.triple).join(', ')}`);
  process.exit(1);
}

// ---------- helpers ----------

function step(label) {
  console.log(`\n>> ${label}`);
}

function run(cmd, args, opts = {}) {
  if (OPTS.dryRun) {
    console.log(`  [dry-run] ${cmd} ${args.join(' ')}`);
    return { status: 0, stdout: '', stderr: '' };
  }
  const r = spawnSync(cmd, args, { stdio: 'inherit', ...opts });
  if (r.status !== 0) {
    console.error(`  command failed (exit ${r.status}): ${cmd} ${args.join(' ')}`);
    process.exit(2);
  }
  return r;
}

function runCapture(cmd, args, opts = {}) {
  // Preflight version checks must always run (even in dry-run mode); use this
  // helper only for read-only commands.
  return execFileSync(cmd, args, { encoding: 'utf8', ...opts });
}

function ensureDir(d) {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

function rmDir(d) {
  if (fs.existsSync(d)) fs.rmSync(d, { recursive: true, force: true });
}

function sha256(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

// ---------- preflight ----------

step('Preflight');

if (!fs.existsSync(ENTRY)) {
  console.error(`  ERROR: entry not found: ${ENTRY}`);
  process.exit(1);
}

try {
  const v = runCapture('bun', ['--version']).trim();
  console.log(`  bun: ${v}`);
  // Pin a sane minimum. As of writing pipeline tested on 1.3.13.
  const [maj, min] = v.split('.').map(Number);
  if (maj < 1 || (maj === 1 && min < 3)) {
    console.error(`  ERROR: bun >= 1.3 required; found ${v}`);
    process.exit(1);
  }
} catch (e) {
  console.error('  ERROR: `bun` not found in PATH. Install from https://bun.com');
  process.exit(1);
}

if (!OPTS.skipObfuscate) {
  try {
    require.resolve('javascript-obfuscator', { paths: [REPO_ROOT] });
    console.log('  javascript-obfuscator: present');
  } catch {
    console.error('  ERROR: javascript-obfuscator not installed. Run `npm install` in repo root first.');
    process.exit(1);
  }
}

const releaseVersion = process.env.RELEASE_VERSION
  || JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'package.json'), 'utf8')).version;
console.log(`  release version: ${releaseVersion}`);
console.log(`  targets: ${TARGETS.map(t => t.name).join(', ')}`);
console.log(`  out dir: ${OUT_DIR}`);
if (OPTS.skipObfuscate) console.log('  WARN: --skip-obfuscate => DEV-grade binary, do NOT distribute');
if (OPTS.dryRun) console.log('  mode: DRY RUN (no files will change)');

// ---------- stage 1: bun bundle ----------

step('Stage 1 — bun bundle (resolve require tree to one file)');

ensureDir(STAGE_DIR);
const BUNDLED_JS = path.join(STAGE_DIR, 'bundled.js');

// `--external '@napi-rs/keyring'`: keyring is an optional dep loaded via
// dynamic require() in workspace-id; bun otherwise tries to bundle the
// platform-specific `.node` file as a second output asset, which makes
// `bun build … --outfile=…` fail with "cannot write multiple output files
// without an output directory". Treating it as external preserves the
// existing optional-fallback behaviour (require throws → FS path used) in
// the standalone binaries.
run('bun', ['build', ENTRY, '--target=node', `--outfile=${BUNDLED_JS}`, '--external', '@napi-rs/keyring']);

const bundleSize = OPTS.dryRun ? 0 : fs.statSync(BUNDLED_JS).size;
console.log(`  bundled.js: ${(bundleSize / 1024 / 1024).toFixed(2)} MB`);

// ---------- stage 2: obfuscate ----------

let payloadJs = BUNDLED_JS;

if (!OPTS.skipObfuscate) {
  step('Stage 2 — javascript-obfuscator (high strength, bundler-safe)');
  const OBF_JS = path.join(STAGE_DIR, 'bundled.obf.js');

  if (!OPTS.dryRun) {
    const O = require(require.resolve('javascript-obfuscator', { paths: [REPO_ROOT] }));
    const src = fs.readFileSync(BUNDLED_JS, 'utf8');
    // Seed obfuscation from release version: gives same-version reruns a
    // narrow PRNG path, but the obfuscator has internal non-determinism
    // beyond the seed (Set iteration / stringArray rotation timing) so two
    // runs with the same seed can still differ slightly. Empirically ~5%
    // of those runs emit invalid syntax (e.g. mangling `new.target` to
    // `#target`, which then crashes `bun compile`). Validate after each
    // attempt and retry — see RETRY note in pipeline rationale below.
    const baseSeed = parseInt(crypto.createHash('sha256').update(`evolver:${releaseVersion}`).digest('hex').slice(0, 8), 16);
    const obfOpts = {
      compact: true,
      controlFlowFlattening: true,
      controlFlowFlatteningThreshold: 0.75,
      deadCodeInjection: true,
      deadCodeInjectionThreshold: 0.4,
      stringArray: true,
      stringArrayEncoding: ['rc4'],
      stringArrayThreshold: 0.85,
      identifierNamesGenerator: 'hexadecimal',
      // The next three MUST stay disabled — they are incompatible with bun's
      // standalone wrapping (selfDefending + transformObjectKeys + renameGlobals
      // each break either compile-time bundling or run-time module resolution).
      // See pipeline notes at top of file.
      renameGlobals: false,
      selfDefending: false,
      transformObjectKeys: false,
      debugProtection: false,
      splitStrings: true,
      splitStringsChunkLength: 8,
      numbersToExpressions: true,
      unicodeEscapeSequence: true,
      target: 'node',
    };

    const MAX_OBF_ATTEMPTS_RAW = process.env.OBF_MAX_ATTEMPTS;
    // Default 12 (was 4). The obfuscator's new.target -> #target mangling is
    // non-deterministic ACROSS PROCESSES, not just across seeds: the same seed
    // + same input can pass in one node process and fail in another (Set
    // iteration / internal-state timing). So perturbing the seed per attempt is
    // not the real lever — re-running the obfuscate call is. The v1.87.4 deploy
    // hit 4/4 consecutive failures with the default of 4 and aborted the npm
    // publish + binary upload. At an observed per-attempt failure rate that can
    // run well above the historical ~5% for some bundles, 4 retries is too few;
    // 12 drives the all-fail probability to negligible while costing only extra
    // attempts on the rare unlucky run. Override with OBF_MAX_ATTEMPTS.
    const MAX_OBF_ATTEMPTS = MAX_OBF_ATTEMPTS_RAW === undefined
      ? 12
      : parseInt(MAX_OBF_ATTEMPTS_RAW, 10);
    if (!Number.isInteger(MAX_OBF_ATTEMPTS) || MAX_OBF_ATTEMPTS < 1) {
      console.error(`  ERROR: OBF_MAX_ATTEMPTS must be a positive integer; got ${JSON.stringify(MAX_OBF_ATTEMPTS_RAW)}.`);
      process.exit(1);
    }
    let attempt = 0;
    let usedSeed = baseSeed;
    let lastValidationErr = null;
    let succeeded = false;
    while (attempt < MAX_OBF_ATTEMPTS) {
      attempt++;
      // Perturb seed on retries to dodge a stuck PRNG path. Attempt 1 keeps
      // the canonical seed for best-effort reproducibility; later attempts
      // shift by attempt index so the next deploy gets a fresh trajectory.
      usedSeed = baseSeed + (attempt - 1);
      const t0 = Date.now();
      const result = O.obfuscate(src, { ...obfOpts, seed: usedSeed });
      fs.writeFileSync(OBF_JS, result.getObfuscatedCode());
      const obfSize = fs.statSync(OBF_JS).size;
      const obfSecs = ((Date.now() - t0) / 1000).toFixed(1);

      const check = spawnSync('node', ['--check', OBF_JS], { encoding: 'utf8' });
      if (check.status !== 0) {
        lastValidationErr = (check.stderr || check.stdout || '').split('\n').slice(0, 3).join(' | ');
        console.warn(`  attempt ${attempt}/${MAX_OBF_ATTEMPTS}: obfuscator output failed node --check (${lastValidationErr.slice(0, 200)}); retrying with perturbed seed...`);
        continue;
      }
      // Second gate: bun's compile-time parser is stricter than node's.
      // 1.87.x (post `@napi-rs/keyring` dep) revealed that ~5% of obfuscator
      // outputs that pass `node --check` still trip bun with errors like
      // `Expected "in" but found ","`. Probe with a cheap bundle-only call
      // (no --compile, native target) to fail fast and feed back into the
      // seed-perturbation loop instead of dying in stage 3.
      const bunProbe = spawnSync('bun', [
        'build', OBF_JS,
        '--target=bun',
        `--outfile=${path.join(STAGE_DIR, 'bundled.obf.bunprobe.js')}`,
      ], { encoding: 'utf8' });
      if (bunProbe.status !== 0) {
        lastValidationErr = (bunProbe.stderr || bunProbe.stdout || '').split('\n').slice(0, 3).join(' | ');
        console.warn(`  attempt ${attempt}/${MAX_OBF_ATTEMPTS}: obfuscator output rejected by bun parser (${lastValidationErr.slice(0, 200)}); retrying with perturbed seed...`);
        continue;
      }
      console.log(`  obfuscation: ${obfSecs}s, output ${(obfSize / 1024 / 1024).toFixed(2)} MB (attempt ${attempt}/${MAX_OBF_ATTEMPTS}, seed=0x${usedSeed.toString(16)})`);
      succeeded = true;
      break;
    }
    if (!succeeded) {
      console.error(`  ERROR: javascript-obfuscator produced syntactically invalid output in ${MAX_OBF_ATTEMPTS} attempts.`);
      console.error(`         last error: ${lastValidationErr || '(none — loop did not run)'}`);
      console.error(`         raise OBF_MAX_ATTEMPTS env var to retry more times, or temporarily run with --skip-obfuscate.`);
      process.exit(2);
    }
  } else {
    console.log('  [dry-run] would obfuscate stage/bundled.js -> stage/bundled.obf.js (with retry-on-syntax-error)');
  }

  payloadJs = OBF_JS;
} else {
  console.log('\n>> Stage 2 — SKIPPED (--skip-obfuscate)');
}

// ---------- stage 3: per-target compile ----------

step(`Stage 3 — bun compile (${TARGETS.length} target${TARGETS.length === 1 ? '' : 's'})`);

// Idempotency: scrub OUT_DIR up front so stale binaries from a prior partial
// run can't leak into a subsequent `gh release upload dist-binaries/*`.
if (!OPTS.dryRun) {
  rmDir(OUT_DIR);
}
ensureDir(OUT_DIR);
const sums = [];

for (const t of TARGETS) {
  const outPath = path.join(OUT_DIR, t.name);
  console.log(`\n  --- ${t.triple} -> ${path.relative(REPO_ROOT, outPath)} ---`);

  run('bun', [
    'build',
    payloadJs,
    '--compile',
    '--minify',
    `--target=${t.triple}`,
    `--outfile=${outPath}`,
  ]);

  if (!OPTS.dryRun) {
    const stat = fs.statSync(outPath);
    fs.chmodSync(outPath, 0o755);
    const hash = sha256(outPath);
    fs.writeFileSync(`${outPath}.sha256`, `${hash}  ${t.name}\n`);
    sums.push(`${hash}  ${t.name}`);
    console.log(`    size: ${(stat.size / 1024 / 1024).toFixed(1)} MB   sha256: ${hash.slice(0, 16)}…`);
  }
}

// Smoke test only the host platform binary (cross-platform binaries cannot
// be executed on the build host without an emulator; skip them by design).
const hostTriple = (() => {
  const arch = process.arch === 'arm64' ? 'arm64' : 'x64';
  const plat = process.platform === 'darwin' ? 'darwin'
             : process.platform === 'linux'  ? 'linux'
             : process.platform === 'win32'  ? 'windows'
             : null;
  return plat ? `${plat}-${arch}` : null;
})();

if (!OPTS.dryRun && hostTriple) {
  // Match against the triple suffix (e.g. "darwin-arm64"), since the binary
  // name on Windows includes a ".exe" extension.
  const hostBin = TARGETS.find(t => t.triple.endsWith(hostTriple));
  if (hostBin) {
    step(`Stage 4 — smoke test ${hostBin.name}`);
    const r = spawnSync(path.join(OUT_DIR, hostBin.name), ['--help'], {
      timeout: 15000,
      encoding: 'utf8',
    });
    if (r.status !== 0 || !r.stdout || !r.stdout.includes('Usage:')) {
      console.error('  ERROR: smoke test failed.');
      console.error(`    exit: ${r.status}`);
      console.error(`    stdout: ${(r.stdout || '').slice(0, 200)}`);
      console.error(`    stderr: ${(r.stderr || '').slice(0, 200)}`);
      process.exit(3);
    }
    console.log('  smoke test: OK');
  }
}

// ---------- write combined SHA256SUMS ----------

if (!OPTS.dryRun) {
  step('Writing combined SHA256SUMS.txt');
  const sumsFile = path.join(OUT_DIR, 'SHA256SUMS.txt');
  fs.writeFileSync(sumsFile, sums.join('\n') + '\n');
  console.log(`  wrote ${path.relative(REPO_ROOT, sumsFile)}`);
}

// ---------- cleanup ----------

if (!OPTS.keepStage && !OPTS.dryRun) {
  rmDir(STAGE_DIR);
} else if (OPTS.keepStage) {
  console.log(`\n  (kept stage at ${path.relative(REPO_ROOT, STAGE_DIR)} for inspection)`);
}

step(`Done. ${TARGETS.length} binar${TARGETS.length === 1 ? 'y' : 'ies'} in ${path.relative(REPO_ROOT, OUT_DIR)}/`);
console.log('  next: gh release upload v<ver> dist-binaries/* --repo EvoMap/evolver');

//
// =====================================================================
//  PIPELINE RATIONALE — 2026-05-05
// =====================================================================
//
// Why "bun-bundle then obfuscate" rather than the more obvious
// "obfuscate src/ then bun-bundle":
//
//   javascript-obfuscator at high strength (stringArray + RC4 +
//   transformObjectKeys + ...) rewrites string literals through a runtime
//   lookup function: require('./gep/paths') becomes
//   require(_0xLOOKUP(0x82b)). Bun's bundler does static analysis on
//   require() arguments at compile time, so it cannot resolve those
//   dynamic require calls and the resulting binary throws "Cannot find
//   module './gep/paths'" on first invocation.
//
//   By bundling FIRST, every require() is inlined and resolved before the
//   obfuscator ever sees the code. The obfuscator then operates on a
//   single self-contained file with no remaining dynamic requires, so
//   stringArray and friends are safe.
//
// Why selfDefending must stay OFF:
//
//   selfDefending: true injects a guard that hangs (infinite while loop)
//   when it detects formatting changes. bun --compile wraps the JS payload
//   in a standalone executable container that re-emits the source with
//   different whitespace + line endings, which trips the guard immediately.
//   Symptom: binary launches, opens stdio, then never exits.
//
// Why transformObjectKeys must stay OFF:
//
//   Same family of issue — it rewrites top-level module.exports / exports
//   patterns in ways that bun's standalone runtime cannot rebuild.
//
// Why renameGlobals must stay OFF:
//
//   Not strictly required after the bundle step (no external require'd
//   modules remain), but kept off as a safety belt; the cost is small
//   because identifier hashing already covers >99% of names through
//   identifierNamesGenerator='hexadecimal'.
//
// Smoke test policy:
//
//   We only smoke test the binary that matches the BUILD HOST triple.
//   Cross-compiled binaries can't be executed without an emulator
//   (qemu-user-static on linux, Rosetta on darwin-x64-on-arm64). CI/CD
//   in GitHub Actions on `runs-on: macos-latest, ubuntu-latest` should
//   set up the matrix so each runner smoke-tests its own native target.
//
// Stage 2 retry-on-syntax-error (added 2026-05-22, v1.85.0 deploy
// post-mortem):
//
//   The v1.85.0 release deploy hit `bun compile` failing with
//   `Expected "in" but found ","` at offset ~1.5MB into bundled.obf.js.
//   The failing region contained `(#target,this)` — javascript-obfuscator
//   had mangled `new.target` into `#target` (a private class field syntax
//   that's only legal inside a class body). A from-scratch rebuild on the
//   same source + seed produced a different output (15.18 MB vs 15.14 MB)
//   that compiled cleanly, confirming the obfuscator has internal
//   non-determinism beyond the user-supplied seed.
//
//   Mitigation: after each obfuscation attempt, run `node --check` on the
//   output; if syntax is invalid, perturb the seed by +attempt and retry
//   up to OBF_MAX_ATTEMPTS times (default 4). Cost of validation is
//   ~1 second on 15 MB; cost of catching the failure here vs after a
//   doomed bun compile pass is roughly 50s saved per failure.
//

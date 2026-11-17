#!/usr/bin/env node
/**
 * full-cycle.js — Run a complete evolver cycle (V1 + V2).
 *
 * V1 flow: evolver run → capture GEP → agent executes → evolver solidify (deprecated)
 * V2 flow: evolver ingest → evolver distill → evolver cycle (requires runner)
 *
 * Usage:
 *   node skills/evolver-bridge/scripts/full-cycle.js        # V1 run
 *   node skills/evolver-bridge/scripts/full-cycle.js --v2   # V2 ingest + distill
 *   node skills/evolver-bridge/scripts/full-cycle.js --status  # show cycle status
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE_ROOT || process.cwd();
const EVOLUTION_DIR = path.join(WORKSPACE, 'memory', 'evolution');
const LOG_DIR = path.join(WORKSPACE, 'memory', 'evolution', 'logs');

function log(msg) {
  const ts = new Date().toISOString();
  const line = `[${ts}] [evolver-bridge] ${msg}`;
  console.log(line);
  try {
    fs.appendFileSync(path.join(LOG_DIR, 'full-cycle.log'), line + '\n', 'utf-8');
  } catch (_) {}
}

function runCmd(cmd, opts = {}) {
  const merged = { cwd: WORKSPACE, timeout: 120_000, encoding: 'utf-8', ...opts };
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return execSync(cmd, merged);
    } catch (e) {
      lastErr = e;
      log(`Attempt ${attempt}/3 failed: ${e.message}`);
      if (attempt < 3) {
        const delay = attempt * 2000;
        log(`Retrying in ${delay}ms...`);
        execSync(`sleep ${delay / 1000}`);
      }
    }
  }
  throw lastErr;
}

// ── V1 Flow ──────────────────────────────────────────────
function v1Run() {
  log('Starting V1 evolution cycle...');

  const outFile = path.join(EVOLUTION_DIR, 'last_run_stdout.txt');
  fs.mkdirSync(EVOLUTION_DIR, { recursive: true });

  log('Step 1: evolver run');
  let raw;
  try {
    raw = runCmd('evolver run');
    fs.writeFileSync(outFile, raw, 'utf-8');
  } catch (e) {
    if (e.stdout) {
      raw = e.stdout;
      fs.writeFileSync(outFile, raw, 'utf-8');
    }
    if (!fs.existsSync(outFile) || fs.statSync(outFile).size === 0) {
      log(`evolver run failed: ${e.message}`);
      process.exit(1);
    }
    raw = fs.readFileSync(outFile, 'utf-8');
  }

  const gepStart = raw.indexOf('GEP');
  const gepEnd = raw.indexOf('Evolver finished.');

  if (gepStart === -1) {
    log('WARN: no GEP prompt found in evolver run output (V1 deprecated)');
    log('Trying to read existing GEP files from memory/evolution/...');
    const existingGeps = fs.readdirSync(EVOLUTION_DIR)
      .filter((f) => f.startsWith('gep_prompt_') && f.endsWith('.txt'))
      .sort()
      .reverse();
    if (existingGeps.length > 0) {
      const latestGep = path.join(EVOLUTION_DIR, existingGeps[0]);
      log(`Using existing GEP: ${existingGeps[0]}`);
      console.log(`\n=== Using existing GEP: ${existingGeps[0]} ===`);
      console.log(`File: ${latestGep}`);
      log('V1 cycle complete (using existing GEP). Run V2 with --v2 for new cycles.');
    } else {
      log('No GEP files found. Use --v2 for V2 material-driven cycles.');
      console.log('\n=== No GEP available ===');
      console.log('V1 is deprecated. Use: node full-cycle.js --v2');
    }
    return;
  }

  const gep = raw.slice(gepStart, gepEnd > gepStart ? gepEnd : undefined).trim();
  const cycleId = (gep.match(/Cycle #(\d+)/) || [])[1] || '????';
  const geneId = (gep.match(/Selected Gene "([^"]+)"/) || [])[1] || 'unknown';
  let signals = [];
  try {
    const m = gep.match(/Context \[Signals\]:\s*\n(\[[\s\S]*?\])/);
    if (m) signals = JSON.parse(m[1]);
  } catch (_) {}

  const runId = `run_${Date.now()}`;
  const filename = `gep_prompt_Cycle_#${cycleId.padStart(4, '0')}_${runId}.txt`;
  fs.writeFileSync(path.join(EVOLUTION_DIR, filename), gep, 'utf-8');
  log(`Saved GEP prompt: ${filename} (${gep.length} bytes)`);

  fs.writeFileSync(
    path.join(EVOLUTION_DIR, 'cycle_progress.json'),
    JSON.stringify({
      cycleId: cycleId.padStart(4, '0'),
      status: 'executing',
      started_at: new Date().toISOString(),
      gene_id: geneId,
      run_id: runId,
      prompt_file: filename,
      signals,
    }, null, 2),
    'utf-8',
  );

  console.log(`\n=== CYCLE #${cycleId} ===`);
  console.log(`Gene   : ${geneId}`);
  console.log(`Signals: ${signals.join(', ')}`);
  console.log(`Prompt : ${path.join(EVOLUTION_DIR, filename)}`);
  log('V1 cycle complete. Execute the plan, then run: evolver solidify');
}

// ── V2 Flow ──────────────────────────────────────────────
function v2Run() {
  log('Starting V2 evolution cycle (material-driven)...');

  fs.mkdirSync(EVOLUTION_DIR, { recursive: true });
  const transcripts = fs.readdirSync(EVOLUTION_DIR)
    .filter((f) => /\.(transcript|chat|messages)\.jsonl?$/i.test(f));

  if (transcripts.length === 0) {
    log('ERROR: no *.transcript.jsonl found. Run session-to-material first.');
    process.exit(1);
  }

  transcripts.sort((a, b) =>
    fs.statSync(path.join(EVOLUTION_DIR, b)).mtimeMs -
    fs.statSync(path.join(EVOLUTION_DIR, a)).mtimeMs
  );

  const transcript = path.join(EVOLUTION_DIR, transcripts[0]);
  log(`Material source: ${path.basename(transcript)}`);

  // Step 1: ingest
  log('Step 1: evolver ingest');
  try {
    const out = runCmd(`evolver ingest "${transcript}"`);
    process.stdout.write(out);
  } catch (e) {
    log(`ingest failed: ${e.message}`);
    if (!e.message.includes('unchanged since last ingest')) {
      process.exit(1);
    }
    log('Material unchanged, continuing...');
  }

  // Step 2: distill
  log('Step 2: evolver distill');
  try {
    const out = runCmd('evolver distill');
    process.stdout.write(out);
    const geneMatch = out.match(/distilled gene (\S+)/);
    if (geneMatch) {
      log(`New gene: ${geneMatch[1]}`);
    }
  } catch (e) {
    log(`distill failed: ${e.message}`);
    process.exit(1);
  }

  log('V2 cycle complete. Run evolver review to approve new genes.');
}

// ── Status ───────────────────────────────────────────────
function showStatus() {
  log('Checking evolver status...');
  try {
    const out = runCmd('evolver cycle status --json');
    const status = JSON.parse(out);
    console.log(JSON.stringify(status, null, 2));
  } catch (e) {
    log(`status check failed: ${e.message}`);
  }
  try {
    const out = runCmd('evolver review --json');
    console.log(out);
  } catch (e) {
    log(`review check failed: ${e.message}`);
  }
}

// ── Main ─────────────────────────────────────────────────
function main() {
  fs.mkdirSync(LOG_DIR, { recursive: true });

  const args = process.argv.slice(2);
  if (args.includes('--v2')) {
    v2Run();
  } else if (args.includes('--status')) {
    showStatus();
  } else {
    v1Run();
  }
}

main();

#!/usr/bin/env node
/**
 * monitor.js - Skill Evolver v2.0 Continuous Mode Monitor
 *
 * Zero-token incremental check: scans new sessions since last evolution,
 * counts pending SIs, decides whether to trigger evolution.
 *
 * Called by OS crontab (every 4h in continuous mode). Not called in manual/scheduled modes.
 *
 * Logic:
 *   1. Read evolver-state.json + evolver-config.json
 *   2. Scan sessions modified since last_evolution_ts
 *   3. Quick SI detection (anchor points only, no full trace extraction)
 *   4. If pending >= minNewSI or time > maxInterval → trigger
 *   5. If triggered: run N batches of run-daily.sh (ceil(pending / maxSIPerRun))
 *   6. Update evolver-state.json
 *   7. Send notification via configured hook (if any)
 *
 * Usage:
 *   node monitor.js [--config <path>] [--state <path>] [--sessions-dir <path>] [--dry-run]
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const SCRIPT_DIR = __dirname;
const EVOLVER_DIR = path.resolve(SCRIPT_DIR, '..');
const DEFAULT_CONFIG_PATH = path.join(EVOLVER_DIR, 'evolver-config.json');
const DEFAULT_STATE_PATH = path.join(EVOLVER_DIR, 'evolver-state.json');

// ─── Config / State Loading ────────────────────────────────────

const DEFAULT_CONFIG = {
  mode: 'continuous',
  monitor: { interval: '4h' },
  trigger: {
    minNewSI: 5,
    maxInterval: '7d',
  },
  budget: {
    maxSIPerRun: 20,
    model: 'auto',
  },
  notifications: {
    level: 'brief',        // off | brief | verbose
    hook: null,             // http(s) webhook URL or null = log only (shell-command hooks removed in v2.4.11 for security)
    frequency: '1d',
  },
};

const DEFAULT_STATE = {
  initialized: false,
  last_evolution_ts: null,
  last_monitor_ts: null,
  processed_sessions: [],
  pending_si_count: 0,
  total_evolutions: 0,
  total_si_processed: 0,
  paused: false,
  carry_over_since: null,   // original since ts when carry-over is pending
  carry_over_offset: 0,     // number of SIs already processed in carry-over
};

function loadJSON(filePath, defaults) {
  if (!fs.existsSync(filePath)) return { ...defaults };
  try {
    return { ...defaults, ...JSON.parse(fs.readFileSync(filePath, 'utf8')) };
  } catch {
    console.error(`[monitor] Warning: could not parse ${filePath}, using defaults`);
    return { ...defaults };
  }
}

function saveJSON(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function parseInterval(str) {
  if (!str) return 0;
  const match = str.match(/^(\d+)\s*(d|h|m|s)$/i);
  if (!match) return 0;
  const num = parseInt(match[1]);
  const unit = match[2].toLowerCase();
  return num * ({ d: 86400000, h: 3600000, m: 60000, s: 1000 }[unit] || 0);
}

// ─── Quick SI Detection ────────────────────────────────────────

const { getAdapter } = require('./lib/platform-detect');

// countSIsInSession removed - SI counting now delegated to trace-extractor --count-only
// This ensures monitor and pipeline use identical detection logic (v2.0.2)

// ─── Auto-detect Sessions Dir ──────────────────────────────────

function detectSessionsDir() {
  // Cross-platform: try adapter-based detection first.
  // Returns comma-separated dirs when multiple exist (e.g. multi-channel layouts).
  try {
    const adapter = getAdapter();
    const adapterPaths = adapter.detectPaths().filter(dir => {
      try { return fs.statSync(dir).isDirectory(); } catch { return false; }
    });
    if (adapterPaths.length > 0) return adapterPaths.join(',');
  } catch (err) {
    // Adapter detection failed, fall through to legacy paths
  }

  // Legacy fallback: hardcoded OpenClaw paths
  const candidates = [];
  if (process.env.OPENCLAW_STATE_DIR) {
    candidates.push(path.join(process.env.OPENCLAW_STATE_DIR, 'agents/main/sessions'));
  }
  const ocRoot = path.resolve(EVOLVER_DIR, '..', '..');
  candidates.push(path.join(ocRoot, 'agents/main/sessions'));
  candidates.push(path.join(process.env.HOME || '/root', '.openclaw/agents/main/sessions'));

  for (const dir of candidates) {
    if (fs.existsSync(dir)) {
      const files = fs.readdirSync(dir).filter(f => f.endsWith('.jsonl'));
      if (files.length > 0) return dir;
    }
  }
  for (const dir of candidates) {
    if (fs.existsSync(dir)) return dir;
  }
  return null;
}

// ─── Main ──────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);

  let configPath = DEFAULT_CONFIG_PATH;
  let statePath = DEFAULT_STATE_PATH;
  let sessionsDir = null;
  let dryRun = false;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--config':       configPath = args[++i]; break;
      case '--state':        statePath = args[++i]; break;
      case '--sessions-dir': sessionsDir = args[++i]; break;
      case '--dry-run':      dryRun = true; break;
    }
  }

  const config = loadJSON(configPath, DEFAULT_CONFIG);
  const state = loadJSON(statePath, DEFAULT_STATE);

  // Check preconditions
  if (state.paused) {
    console.error('[monitor] Paused. Skipping.');
    process.exit(0);
  }

  if (config.mode !== 'continuous') {
    console.error(`[monitor] Mode is "${config.mode}", not continuous. Skipping.`);
    process.exit(0);
  }

  // Detect sessions dir
  if (!sessionsDir) sessionsDir = detectSessionsDir();
  // Validate: for comma-separated multi-dir, check at least one exists
  if (!sessionsDir) {
    console.error('[monitor] Sessions dir not found. Skipping.');
    process.exit(0);
  }
  const sessionsDirList = sessionsDir.split(',').filter(d => fs.existsSync(d));
  if (sessionsDirList.length === 0) {
    console.error(`[monitor] No valid sessions dirs found in: ${sessionsDir}. Skipping.`);
    process.exit(0);
  }
  sessionsDir = sessionsDirList.join(','); // normalized: only valid dirs

  // Determine cutoff: sessions modified since last evolution
  const lastEvoTs = state.last_evolution_ts ? new Date(state.last_evolution_ts).getTime() : 0;

  // First run: initialize state and exit - first evolution is user-initiated via SKILL.md guidance
  if (lastEvoTs === 0) {
    state.last_evolution_ts = new Date().toISOString();
    state.initialized = true;
    state.last_monitor_ts = new Date().toISOString();
    saveJSON(statePath, state);
    console.error('[monitor] First run: initialized state, entering incremental mode. First evolution is user-initiated.');
    console.log(JSON.stringify({ trigger: false, pending_si: 0, status: 'initialized' }));
    process.exit(0);
  }

  // Use trace-extractor --count-only for SI detection (unified logic with extraction pipeline)
  const extractorPath = path.join(SCRIPT_DIR, 'trace-extractor.js');
  const countArgs = ['--sessions-dir', sessionsDir, '--count-only'];

  // Carry-over: if previous run left unprocessed SIs, use original since timestamp
  const effectiveSince = state.carry_over_since || state.last_evolution_ts;
  if (effectiveSince) {
    countArgs.push('--since', effectiveSince);
  } else {
    countArgs.push('--window-days', '7');
  }

  let totalNewSI = 0;
  let siSkills = {};
  try {
    const countOutput = require('child_process').execFileSync(
      process.execPath, [extractorPath, ...countArgs],
      { encoding: 'utf8', timeout: 30000 }
    );
    const countResult = JSON.parse(countOutput.trim());
    const rawCount = countResult.count || 0;
    siSkills = countResult.skills || {};
    // Subtract carry-over offset: count-only returns total SIs in window,
    // but some may have been processed in previous batches
    const carryOffset = state.carry_over_offset || 0;
    totalNewSI = Math.max(0, rawCount - carryOffset);
    if (carryOffset > 0) {
      console.error(`[monitor] Raw SI count: ${rawCount}, carry-over offset: ${carryOffset}, effective: ${totalNewSI}`);
    }
  } catch (err) {
    console.error(`[monitor] SI count via extractor failed: ${err.message}`);
    console.error(`[monitor] Falling back to 0 SIs (will retry next cycle)`);
    totalNewSI = 0;
  }

  console.error(`[monitor] ${totalNewSI} pending SIs detected (via trace-extractor --count-only)`);
  if (Object.keys(siSkills).length > 0) {
    console.error(`[monitor] Skills: ${Object.entries(siSkills).map(([k,v]) => `${k}(${v})`).join(', ')}`);
  }

  // Update state
  state.last_monitor_ts = new Date().toISOString();
  state.pending_si_count = totalNewSI;

  // Trigger decision
  const timeSinceLastEvo = Date.now() - (lastEvoTs || 0);
  const maxIntervalMs = parseInterval(config.trigger?.maxInterval || '7d');
  const minNewSI = config.trigger?.minNewSI || 5;
  const maxSIPerRun = config.budget?.maxSIPerRun || 20;

  let shouldTrigger = false;
  let triggerReason = '';

  if (totalNewSI >= minNewSI) {
    shouldTrigger = true;
    triggerReason = `pending SIs (${totalNewSI}) >= minNewSI (${minNewSI})`;
  } else if (lastEvoTs > 0 && timeSinceLastEvo > maxIntervalMs) {
    shouldTrigger = true;
    triggerReason = `time since last evolution (${Math.round(timeSinceLastEvo / 3600000)}h) > maxInterval`;
  }

  if (!shouldTrigger) {
    console.error(`[monitor] No trigger: ${totalNewSI} SIs pending, need ${minNewSI}. Next check in ${config.monitor?.interval || '4h'}.`);
    // stdout: explicit no-trigger signal for cron agent (Brain-Hand protocol)
    console.log(JSON.stringify({ trigger: false, pending_si: totalNewSI, threshold: minNewSI }));
    saveJSON(statePath, state);
    process.exit(0);
  }

  console.error(`[monitor] TRIGGER: ${triggerReason}`);

  if (dryRun) {
    console.error('[monitor] Dry run - would trigger evolution');
    console.log(JSON.stringify({ trigger: true, reason: triggerReason, pending_si: totalNewSI, batches: Math.ceil(totalNewSI / maxSIPerRun) }));
    saveJSON(statePath, state);
    process.exit(0);
  }

  // Run evolution - cap at 1 batch per cron run, remainder carries over to next trigger
  const maxBatchesPerRun = 1;
  const rawBatchCount = Math.ceil(totalNewSI / maxSIPerRun);
  const batchCount = Math.min(rawBatchCount, maxBatchesPerRun);
  if (rawBatchCount > maxBatchesPerRun) {
    console.error(`[monitor] ${rawBatchCount} batches needed, capping at ${maxBatchesPerRun} (remaining ${totalNewSI - maxSIPerRun * maxBatchesPerRun} SIs carry over to next run)`);
  }
  console.error(`[monitor] Running ${batchCount} evolution batch(es) (${maxSIPerRun} SIs each)`);

  const runDailyScript = path.join(SCRIPT_DIR, 'run-daily.sh');

  let totalProcessed = 0;
  let batchErrors = 0;
  let notifyOutput = '';

  for (let batch = 1; batch <= batchCount; batch++) {
    console.error(`\n[monitor] === Batch ${batch}/${batchCount} ===`);

    const args = [
      runDailyScript,
      '--sessions-dir', sessionsDir,
      '--patches-dir', path.join(EVOLVER_DIR, 'eu'),
      '--state', statePath,
      '--max-si', String(maxSIPerRun),
      '--no-state-update',
    ];
    if (effectiveSince) {
      args.push('--since', effectiveSince);
    } else {
      args.push('--window-days', '7');
    }
    if (state.carry_over_offset > 0) {
      args.push('--skip-si', String(state.carry_over_offset));
    }
    if (config.budget?.model && config.budget.model !== 'auto') {
      args.push('--model', config.budget.model);
    }

    let batchStdout = '';
    try {
      batchStdout = execFileSync('bash', args, { stdio: ['pipe', 'pipe', 'inherit'], timeout: 600000, encoding: 'utf8' }); // 10 min timeout per batch
      totalProcessed += maxSIPerRun;

      // After first batch, update since to now for subsequent batches
      state.last_evolution_ts = new Date().toISOString();
    } catch (err) {
      // execSync throws on non-zero exit; stdout may still be available
      if (err.stdout) batchStdout = err.stdout;
      console.error(`[monitor] Batch ${batch} failed: ${err.message}`);
      batchErrors++;
      // Continue with remaining batches despite errors
    }

    // Accumulate notify.js output from run-daily.sh stdout
    if (batchStdout && batchStdout.trim()) {
      notifyOutput += (notifyOutput ? '\n' : '') + batchStdout.trim();
    }

    // Save state after EACH batch (defensive - survives early termination)
    const batchSucceeded = (batchErrors === 0);
    const processedThisBatch = Math.min(maxSIPerRun, totalNewSI - (totalProcessed - maxSIPerRun));
    if (batchSucceeded) {
      state.total_evolutions = (state.total_evolutions || 0) + 1;
      state.total_si_processed = (state.total_si_processed || 0) + processedThisBatch;
    }

    // Carry-over tracking: update offset or clear if all processed
    const totalProcessedSoFar = (state.carry_over_offset || 0) + processedThisBatch;
    const remaining = totalNewSI - processedThisBatch;

    if (remaining > 0) {
      // Still have unprocessed SIs - preserve carry-over window
      state.carry_over_since = effectiveSince || state.last_evolution_ts;
      state.carry_over_offset = totalProcessedSoFar;
      state.pending_si_count = remaining;
      console.error(`[monitor] ${remaining} SIs remaining, carry-over preserved (offset=${totalProcessedSoFar})`);
    } else {
      // All processed - clear carry-over, advance last_evolution_ts
      state.last_evolution_ts = new Date().toISOString();
      state.carry_over_since = null;
      state.carry_over_offset = 0;
      state.pending_si_count = 0;
    }

    saveJSON(statePath, state);
    console.error(`[monitor] State saved after batch ${batch} (${batchSucceeded ? 'ok' : 'error'})`);
  }

  console.error(`\n[monitor] Complete: ${batchCount - batchErrors}/${batchCount} batches succeeded, ~${Math.min(totalProcessed, totalNewSI)} SIs processed`);

  // Build summary
  const summary = {
    trigger: true,
    timestamp: new Date().toISOString(),
    trigger_reason: triggerReason,
    batches_total: batchCount,
    batches_succeeded: batchCount - batchErrors,
    si_processed: Math.min(totalProcessed, totalNewSI),
  };

  console.log(JSON.stringify(summary));
  if (notifyOutput) {
    console.log(notifyOutput);
  }

  const notifyLevel = config.notifications?.level || 'brief';
  const hook = config.notifications?.hook || config.notifications?.verbose_hook || null;

  // Verbose: push raw results immediately via hook
  if (notifyLevel === 'verbose' && hook) {
    const message = notifyOutput
      ? notifyOutput
      : `🧬 Skill Evolver: ${summary.si_processed} traces processed (${triggerReason})`;
    sendNotification(hook, message);
  }

  // Brief/Verbose: write pending_brief to state for agent consumption.
  // Also attempt immediate delivery via hook if available.
  if (notifyLevel !== 'off' && summary.si_processed > 0) {
    writePendingBrief(statePath, state, config, hook);
  }
}

/**
 * Generate brief data and write to evolver-state.json as pending_brief.
 * If a hook is available, also attempt immediate delivery.
 *
 * Consumption:
 *   - OpenClaw: hook runs `openclaw agent` which triggers agent to deliver
 *   - Claude Code / others: checked on next manual interaction
 */
function writePendingBrief(statePath, state, config, hook) {
  try {
    // Generate brief data via brief-data.js
    const briefDataScript = path.join(EVOLVER_DIR, 'scripts', 'brief-data.js');
    const briefData = require('child_process').execFileSync(
      process.execPath, [briefDataScript],
      { encoding: 'utf8', timeout: 15000, stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim();

    if (!briefData || !briefData.includes('<brief_data>')) {
      console.error('[monitor] No brief data generated (no changes since last brief)');
      return;
    }

    // Write to state (state is passed by reference - this save includes all prior mutations from main())
    state.pending_brief = {
      data: briefData,
      generated_at: new Date().toISOString(),
      delivered: false,
    };
    saveJSON(statePath, state);
    console.error('[monitor] pending_brief written to evolver-state.json');

    // Attempt immediate delivery via hook (if available)
    if (hook) {
      const triggerMsg = `🧬 Skill Evolver has new learnings. Check pending_brief in evolver-state.json and format with brief-prompt.md.`;
      sendNotification(hook, triggerMsg);
      // Don't mark as delivered - let the agent mark it after actual brief generation
    }
  } catch (err) {
    console.error(`[monitor] Failed to generate pending_brief: ${err.message}`);
  }
}

// ─── Notification Hook ──────────────────────────────────────────

/**
 * Send a notification via the configured hook.
 *
 * Hook formats:
 *   - null/undefined: log to stderr only
 *   - URL (http/https): POST JSON { text: message }
 *
 * Note: shell command hooks are not supported. If a non-URL string is
 * configured, a warning is emitted and the message is logged locally only.
 *
 * @param {string|null} hook - notification hook (null or http(s) URL only)
 * @param {string} message - notification text
 */
function sendNotification(hook, message) {
  if (!hook) {
    console.error(`[monitor] Notification (no hook configured, log only):`);
    console.error(`  ${message.split('\n')[0]}`);
    return;
  }

  // Webhook URL
  if (hook.startsWith('http://') || hook.startsWith('https://')) {
    try {
      const url = new URL(hook);
      const lib = url.protocol === 'https:' ? require('https') : require('http');
      const payload = JSON.stringify({ text: message });
      const req = lib.request({
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname + url.search,
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) },
        timeout: 10000,
      }, res => {
        console.error(`[monitor] Webhook notification sent (${res.statusCode})`);
        res.resume();
      });
      req.on('error', err => console.error(`[monitor] Webhook error: ${err.message}`));
      req.write(payload);
      req.end();
    } catch (err) {
      console.error(`[monitor] Webhook notification failed: ${err.message}`);
    }
    return;
  }

  // Non-URL hook: rejected. Shell-command hooks are NOT supported (security:
  // arbitrary command execution removed in v2.4.11). Only http(s) webhook URLs
  // are honored; anything else is logged and ignored.
  console.error(`[monitor] Ignored notification hook: only http(s) webhook URLs are supported (got non-URL value). Shell-command hooks were removed for security.`);
}

main();

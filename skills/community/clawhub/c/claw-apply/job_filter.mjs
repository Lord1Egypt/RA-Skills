#!/usr/bin/env node
import { loadEnv } from './lib/env.mjs';
loadEnv();

/**
 * job_filter.mjs — claw-apply AI Job Filter (Anthropic Batch API)
 *
 * Runs in two phases on each invocation:
 *
 * Phase 1 — COLLECT: if a batch is in flight, check status + download results
 * Phase 2 — SUBMIT:  if no batch pending, find unscored jobs + submit a new batch
 *
 * Designed to run hourly via cron. Safe to run anytime — idempotent.
 *
 * Usage:
 *   node job_filter.mjs           — normal run (collect if pending, else submit)
 *   node job_filter.mjs --stats   — show filter stats only
 */

import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { readFileSync, writeFileSync, existsSync, unlinkSync, createWriteStream } from 'fs';

const __dir = dirname(fileURLToPath(import.meta.url));

// Tee all output to a log file so it's always available regardless of how the process is launched
const logStream = createWriteStream(resolve(__dir, 'data/filter.log'), { flags: 'w' });
const origStdoutWrite = process.stdout.write.bind(process.stdout);
const origStderrWrite = process.stderr.write.bind(process.stderr);
process.stdout.write = (chunk, ...args) => { logStream.write(chunk); return origStdoutWrite(chunk, ...args); };
process.stderr.write = (chunk, ...args) => { logStream.write(chunk); return origStderrWrite(chunk, ...args); };

import { getJobsByStatus, updateJobStatus, loadConfig, loadQueue, saveQueue, dedupeAfterFilter } from './lib/queue.mjs';
import { loadProfile, submitBatches, checkBatch, downloadResults } from './lib/filter.mjs';
import { sendTelegram, formatFilterSummary } from './lib/notify.mjs';
import { DEFAULT_FILTER_MODEL, DEFAULT_FILTER_MIN_SCORE } from './lib/constants.mjs';

const isStats = process.argv.includes('--stats');

const STATE_PATH = resolve(__dir, 'data/filter_state.json');

// ---------------------------------------------------------------------------
// State helpers
// ---------------------------------------------------------------------------

function readState() {
  if (!existsSync(STATE_PATH)) return null;
  try { return JSON.parse(readFileSync(STATE_PATH, 'utf8')); } catch { return null; }
}

function writeState(state) {
  writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function clearState() {
  if (existsSync(STATE_PATH)) unlinkSync(STATE_PATH);
}

// ---------------------------------------------------------------------------
// Stats
// ---------------------------------------------------------------------------

function showStats() {
  const queue = loadQueue();
  const byStatus = {};
  for (const j of queue) byStatus[j.status] = (byStatus[j.status] || 0) + 1;

  const filtered = queue.filter(j => j.status === 'filtered');
  const scored = queue.filter(j => j.filter_score != null);

  console.log('📊 Filter Stats\n');
  console.log(`  New (unfiltered):   ${byStatus['new'] || 0}`);
  console.log(`  Filtered (blocked): ${byStatus['filtered'] || 0}`);
  console.log(`  Total scored:       ${scored.length}`);
  console.log(`  Pass rate:          ${scored.length > 0 ? Math.round((scored.filter(j => j.status !== 'filtered').length / scored.length) * 100) : 0}%\n`);

  const state = readState();
  if (state) {
    const batchIds = state.batches?.map(b => b.batchId).join(', ') || 'none';
    console.log(`  Pending batches: ${batchIds}`);
    console.log(`  Submitted:       ${state.submitted_at}`);
    console.log(`  Job count:       ${state.job_count}\n`);
  }

  if (filtered.length > 0) {
    console.log('Sample filtered:');
    filtered.slice(0, 10).forEach(j =>
      console.log(`  [${j.filter_score}/10] ${j.title} @ ${j.company} — ${j.filter_reason}`)
    );
  }
}

// ---------------------------------------------------------------------------
// Phase 1 — Collect results from all pending batches
// ---------------------------------------------------------------------------

async function collect(state, settings) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  const batches = state.batches; // array of { track, batchId, idMap, jobCount }

  // Check status of all batches
  let allDone = true;
  for (const b of batches) {
    const { status, counts } = await checkBatch(b.batchId, apiKey);
    b._status = status;
    b._counts = counts;
    if (status === 'in_progress') {
      const total = Object.values(counts).reduce((a, v) => a + v, 0);
      const done = (counts.succeeded || 0) + (counts.errored || 0) + (counts.canceled || 0) + (counts.expired || 0);
      console.log(`  [${b.track}] Still processing — ${done}/${total} complete`);
      allDone = false;
    } else {
      console.log(`  [${b.track}] Done — ${counts.succeeded || 0} succeeded, ${counts.errored || 0} errors`);
    }
  }

  if (!allDone) {
    console.log('  Not all batches done yet. Check back later.');
    return;
  }

  // All done — download and merge all results
  console.log('\n  All batches complete. Downloading results...');
  const resultMap = {};
  let totalCost = 0;
  const totalUsage = { input_tokens: 0, output_tokens: 0, cache_creation_input_tokens: 0, cache_read_input_tokens: 0 };
  for (const b of batches) {
    const { results, usage, cost } = await downloadResults(b.batchId, apiKey, b.idMap || {});
    for (const r of results) resultMap[r.jobId] = r;
    totalCost += cost;
    for (const [k, v] of Object.entries(usage)) totalUsage[k] = (totalUsage[k] || 0) + v;
  }

  const searchConfig = loadConfig(resolve(__dir, 'config/search_config.json'));
  const globalMin = searchConfig.filter_min_score ?? DEFAULT_FILTER_MIN_SCORE;

  let passed = 0, filtered = 0, errors = 0;
  const queue = loadQueue();
  const now = new Date().toISOString();

  for (const job of queue) {
    const r = resultMap[job.id];
    if (!r) continue;
    if (job.filter_score != null) continue; // already scored — idempotent

    if (r.error || r.score === null) {
      errors++;
      job.filter_score = null;
      job.filter_reason = r.reason || 'filter_error';
      job.status_updated_at = now;
      continue;
    }

    const track = job.track || 'ae';
    const searchEntry = (searchConfig.searches || []).find(s => s.track === track);
    const minScore = searchEntry?.filter_min_score ?? globalMin;

    job.filter_score = r.score;
    job.filter_reason = r.reason;
    job.status_updated_at = now;

    if (r.score >= minScore) { passed++; }
    else { filtered++; job.status = 'filtered'; }
  }

  saveQueue(queue);

  // Dedup cross-track copies — keep highest-scoring version of each job
  const duped = dedupeAfterFilter();
  if (duped > 0) console.log(`  Deduped ${duped} cross-track copies`);

  clearState();

  // Log run
  const runsPath = resolve(__dir, 'data/filter_runs.json');
  const runs = existsSync(runsPath) ? JSON.parse(readFileSync(runsPath, 'utf8')) : [];
  runs.push({
    batches: batches.map(b => ({ track: b.track, batch_id: b.batchId, job_count: b.jobCount })),
    submitted_at: state.submitted_at,
    collected_at: new Date().toISOString(),
    model: state.model,
    passed,
    filtered,
    errors,
    cost_usd: Math.round(totalCost * 100) / 100,
    usage: totalUsage,
  });
  writeFileSync(runsPath, JSON.stringify(runs, null, 2));

  // Collect top-scoring jobs for summary
  const freshQueue = loadQueue();
  const topJobs = freshQueue
    .filter(j => resultMap[j.id] && j.filter_score >= (searchConfig.filter_min_score ?? DEFAULT_FILTER_MIN_SCORE))
    .sort((a, b) => (b.filter_score || 0) - (a.filter_score || 0))
    .slice(0, 5)
    .map(j => ({ score: j.filter_score, title: j.title, company: j.company }));

  const summary = formatFilterSummary({ passed, filtered, errors, cost: totalCost, topJobs });
  console.log(`\n${summary.replace(/\*/g, '')}`);
  await sendTelegram(settings, summary).catch(() => {});
}

// ---------------------------------------------------------------------------
// Phase 2 — Submit a new batch
// ---------------------------------------------------------------------------

async function submit(settings, searchConfig, candidateProfile) {
  const apiKey = process.env.ANTHROPIC_API_KEY;

  // Get all new jobs that haven't been scored yet (no score AND not already in a pending batch)
  const jobs = getJobsByStatus('new').filter(j => j.filter_score == null && !j.filter_batch_id && !j.filter_submitted_at);

  if (jobs.length === 0) {
    console.log('✅ Nothing to filter — all new jobs already scored.');
    return;
  }

  // Build job profiles map by track
  const profilePaths = settings.filter?.job_profiles || {};
  const jobProfilesByTrack = {};
  for (const [track, path] of Object.entries(profilePaths)) {
    const profile = loadProfile(path);
    if (profile) jobProfilesByTrack[track] = profile;
    else console.warn(`⚠️  Could not load job profile for track "${track}" at ${path}`);
  }

  // Filter out jobs with no profile (will pass through unscored)
  const filterable = jobs.filter(j => jobProfilesByTrack[j.track || 'ae']);
  const noProfile = jobs.length - filterable.length;

  if (noProfile > 0) console.warn(`⚠️  ${noProfile} jobs skipped — no profile for their track`);

  if (filterable.length === 0) {
    console.log('Nothing filterable — no job profiles configured for any track.');
    return;
  }

  const model = settings.filter?.model || DEFAULT_FILTER_MODEL;
  const submittedAt = new Date().toISOString();
  console.log(`🚀 Submitting batches — ${filterable.length} jobs across ${Object.keys(jobProfilesByTrack).length} tracks, model: ${model}`);

  const submitted = await submitBatches(filterable, jobProfilesByTrack, candidateProfile, model, apiKey);

  writeState({
    batches: submitted,
    submitted_at: submittedAt,
    job_count: filterable.length,
    model,
  });

  // Stamp each job with its track's batch ID
  const trackToBatchId = {};
  for (const b of submitted) trackToBatchId[b.track] = b.batchId;

  const allJobs = loadQueue();
  for (const job of allJobs) {
    const batchId = trackToBatchId[job.track || 'ae'];
    if (batchId && !job.filter_batch_id) {
      job.filter_batch_id = batchId;
      job.filter_submitted_at = submittedAt;
    }
  }
  saveQueue(allJobs);

  const batchSummary = submitted.map(b => `${b.track}: ${b.jobCount} jobs`).join(', ');
  console.log(`  ${batchSummary}`);
  console.log(`  Results typically ready in < 1 hour. Next run will collect.`);

  // No Telegram on submit — only notify on collect when results are ready
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  if (isStats) {
    showStats();
    return;
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error('❌ ANTHROPIC_API_KEY not set');
    process.exit(1);
  }

  const settings = loadConfig(resolve(__dir, 'config/settings.json'));
  const searchConfig = loadConfig(resolve(__dir, 'config/search_config.json'));
  const candidateProfile = loadConfig(resolve(__dir, 'config/profile.json'));

  console.log('🔍 claw-apply: AI Job Filter\n');

  const state = readState();

  if (state?.batches?.length > 0) {
    // Phase 1: collect results from pending batches
    await collect(state, settings);
  }

  // Phase 2: submit any remaining unscored jobs (runs after collect too)
  if (!readState()) {
    await submit(settings, searchConfig, candidateProfile);
  }
}

main().then(() => {
  process.exit(0);
}).catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});

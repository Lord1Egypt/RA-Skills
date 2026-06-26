#!/usr/bin/env node
// workflow-template.js — Durable multi-step workflow skeleton
// Copy this file and fill in the step TODOs to build a resilient automation.
//
// Features:
//   - Checkpointed state (survives restarts from any step)
//   - Atomic state writes (tmp → rename, no partial writes)
//   - Exponential backoff + jitter on retries
//   - Timeout wrapper for all async calls
//   - Dead letter queue for unrecoverable failures
//   - Abnormal-exit logging

'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const WORKFLOW_ID    = 'my-workflow';
const STATE_PATH     = process.env.WORKFLOW_STATE_PATH || 'workflow-state.json';
const DLQ_PATH       = process.env.WORKFLOW_DLQ_PATH   || 'workflow-dlq.json';
const STEP_TIMEOUT   = parseInt(process.env.STEP_TIMEOUT_MS, 10) || 30000;

// ---------------------------------------------------------------------------
// Infrastructure: State persistence (atomic writes)
// ---------------------------------------------------------------------------

function loadState(id) {
  try {
    const raw = fs.readFileSync(STATE_PATH, 'utf8');
    const all = JSON.parse(raw);
    return all[id] || {};
  } catch (e) {
    if (e.code === 'ENOENT') return {};
    throw new Error(`Failed to load state from ${STATE_PATH}: ${e.message}`);
  }
}

function saveState(id, state) {
  const tmpPath = STATE_PATH + '.tmp';
  let all = {};
  try {
    if (fs.existsSync(STATE_PATH)) {
      all = JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
    }
  } catch (_) { /* start fresh if corrupted */ }

  all[id] = { ...state, _savedAt: new Date().toISOString() };

  fs.writeFileSync(tmpPath, JSON.stringify(all, null, 2), 'utf8');
  fs.renameSync(tmpPath, STATE_PATH); // atomic on same filesystem
}

// ---------------------------------------------------------------------------
// Infrastructure: Retry with exponential backoff + jitter
// ---------------------------------------------------------------------------

async function withRetry(fn, maxAttempts = 4, baseDelayMs = 1000) {
  let lastError;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e;
      if (attempt === maxAttempts - 1) break;
      const delay = baseDelayMs * Math.pow(2, attempt) + Math.random() * 500;
      console.error(`[retry] attempt ${attempt + 1}/${maxAttempts} failed: ${e.message}. Retrying in ${Math.round(delay)}ms...`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw lastError;
}

// ---------------------------------------------------------------------------
// Infrastructure: Timeout wrapper
// ---------------------------------------------------------------------------

function withTimeout(promise, ms) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Operation timed out after ${ms}ms`)), ms);
    promise.then(
      val => { clearTimeout(timer); resolve(val); },
      err => { clearTimeout(timer); reject(err); }
    );
  });
}

// ---------------------------------------------------------------------------
// Infrastructure: Dead letter queue
// ---------------------------------------------------------------------------

function writeDLQ(item, error) {
  let existing = [];
  try {
    if (fs.existsSync(DLQ_PATH)) {
      existing = JSON.parse(fs.readFileSync(DLQ_PATH, 'utf8'));
    }
  } catch (_) {}
  existing.push({ item, error: error.message, stack: error.stack, failedAt: new Date().toISOString() });
  fs.writeFileSync(DLQ_PATH, JSON.stringify(existing, null, 2), 'utf8');
  console.error(`[dlq] Item written to ${DLQ_PATH}: ${error.message}`);
}

// ---------------------------------------------------------------------------
// Infrastructure: Exit handler
// ---------------------------------------------------------------------------

let workflowStarted = false;
let workflowFinished = false;

process.on('exit', (code) => {
  if (workflowStarted && !workflowFinished) {
    // Write directly to stderr — no async in exit handlers
    process.stderr.write(
      `[workflow:${WORKFLOW_ID}] Abnormal exit (code ${code}) at ${new Date().toISOString()}\n`
    );
  }
});

process.on('uncaughtException', (err) => {
  console.error(`[workflow:${WORKFLOW_ID}] Uncaught exception: ${err.message}`);
  console.error(err.stack);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  console.error(`[workflow:${WORKFLOW_ID}] Unhandled rejection:`, reason);
  process.exit(1);
});

// ---------------------------------------------------------------------------
// Workflow Steps (fill in TODO blocks — infrastructure code is complete)
// ---------------------------------------------------------------------------

async function step1_fetchData(state) {
  if (state.step >= 1) return state;
  console.log('[step 1] Fetching data...');

  // TODO: Replace with your actual data-fetching logic
  const data = await withRetry(
    () => withTimeout(
      Promise.resolve({ records: ['example-item-1', 'example-item-2'] }),
      STEP_TIMEOUT
    )
  );

  state.inputData = data;
  state.step = 1;
  saveState(WORKFLOW_ID, state);
  console.log(`[step 1] Done. Fetched ${data.records.length} records.`);
  return state;
}

async function step2_processItems(state) {
  if (state.step >= 2) return state;
  console.log('[step 2] Processing items...');

  const results = [];
  for (const item of state.inputData.records) {
    try {
      // TODO: Replace with your actual per-item processing logic
      const result = await withRetry(
        () => withTimeout(
          Promise.resolve({ item, processed: true }),
          STEP_TIMEOUT
        )
      );
      results.push(result);
    } catch (e) {
      writeDLQ(item, e);
    }
  }

  state.processedItems = results;
  state.step = 2;
  saveState(WORKFLOW_ID, state);
  console.log(`[step 2] Done. Processed ${results.length}/${state.inputData.records.length} items.`);
  return state;
}

async function step3_writeOutput(state) {
  if (state.step >= 3) return state;
  console.log('[step 3] Writing output...');

  // TODO: Replace with your actual output logic (write to DB, API, file, etc.)
  const outputPath = 'workflow-output.json';
  fs.writeFileSync(outputPath, JSON.stringify(state.processedItems, null, 2), 'utf8');

  state.outputPath = outputPath;
  state.step = 3;
  saveState(WORKFLOW_ID, state);
  console.log(`[step 3] Done. Output written to ${outputPath}.`);
  return state;
}

async function step4_notify(state) {
  if (state.step >= 4) return state;
  console.log('[step 4] Sending notifications...');

  // TODO: Replace with your actual notification logic (email, Telegram, webhook, etc.)
  console.log(`[step 4] Would notify: workflow complete, ${state.processedItems.length} items processed.`);

  state.notifiedAt = new Date().toISOString();
  state.step = 4;
  saveState(WORKFLOW_ID, state);
  console.log('[step 4] Done.');
  return state;
}

// ---------------------------------------------------------------------------
// Main entrypoint
// ---------------------------------------------------------------------------

async function main() {
  workflowStarted = true;
  console.log(`[workflow:${WORKFLOW_ID}] Starting at ${new Date().toISOString()}`);

  let state = loadState(WORKFLOW_ID);
  console.log(`[workflow:${WORKFLOW_ID}] Resuming from step ${state.step || 0}`);

  state = await step1_fetchData(state);
  state = await step2_processItems(state);
  state = await step3_writeOutput(state);
  state = await step4_notify(state);

  workflowFinished = true;

  // Clean up state file on success (optional — comment out to keep for audit)
  // fs.unlinkSync(STATE_PATH);

  console.log(`[workflow:${WORKFLOW_ID}] Completed at ${new Date().toISOString()}`);
}

main().catch(e => {
  console.error(`[workflow:${WORKFLOW_ID}] Fatal error: ${e.message}`);
  process.exit(1);
});

/**
 * Append-only event log for EU lifecycle.
 *
 * Single writer: appendEvent(op, payload). Writes one JSONL line to
 * <skill-evolver-root>/eu-events.jsonl via fs.appendFileSync.
 *
 * Event schema:
 *   { ts: ISO8601, schema: 1, op: <string>, run_id: <string|null>,
 *     eu: <string|null>,  ...op-specific payload }
 *
 * run_id is read from process.env.EVOLVER_RUN_ID at write time; null if absent.
 * Caller supplies `eu` in payload when applicable (e.g. "arxiv-watcher/eu-0042.md").
 *
 * Failure policy: log write failures to stderr but never throw — the
 * audit log must never block main work.
 */

const fs = require('fs');
const path = require('path');

const SCHEMA = 1;

// Resolve events file location relative to skill-evolver root
// (i.e. one level above scripts/). Mirrors how sep-queue.jsonl is resolved.
function eventsPath() {
  return path.join(__dirname, '..', '..', 'eu-events.jsonl');
}

function appendEvent(op, payload = {}) {
  try {
    const record = {
      ts: new Date().toISOString(),
      schema: SCHEMA,
      op,
      run_id: process.env.EVOLVER_RUN_ID || null,
      eu: payload.eu || null,
      ...payload,
    };
    // Ensure eu/run_id appear once in correct order (remove dupes from payload)
    delete record.eu;
    delete record.run_id;
    const ordered = {
      ts: record.ts,
      schema: record.schema,
      op: record.op,
      run_id: process.env.EVOLVER_RUN_ID || null,
      eu: payload.eu || null,
    };
    for (const [k, v] of Object.entries(payload)) {
      if (k === 'eu' || k === 'run_id' || k === 'ts' || k === 'schema' || k === 'op') continue;
      ordered[k] = v;
    }
    fs.appendFileSync(eventsPath(), JSON.stringify(ordered) + '\n', 'utf8');
  } catch (e) {
    // Never crash the main pipeline because audit write failed.
    console.error(`[events] appendEvent(${op}) failed:`, e.message);
  }
}

module.exports = { appendEvent, SCHEMA, eventsPath };
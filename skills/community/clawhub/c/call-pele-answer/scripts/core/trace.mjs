// trace.mjs — per-phase timing for every pe run, appended as one JSON line to
// ~/.call-pele-answer/logs/runs.jsonl (PE_TRACE=0 turns it off; PE_TRACE_FILE moves it).
// Agent-level timing (prompt → tools → answer) comes from hooks/agent-hook.mjs; `pe stats` joins both.
import { appendFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';

export const LOG_DIR = process.env.PE_LOG_DIR || join(homedir(), '.call-pele-answer', 'logs');
export const RUNS = process.env.PE_TRACE_FILE || join(LOG_DIR, 'runs.jsonl');
const now = () => Number(process.hrtime.bigint()) / 1e6;

export function createTrace(cmd) {
  const t0 = now(), spans = [], counts = {};
  let open = null;
  const tr = {
    cmd, meta: {},
    // time a sync or async function under a phase name; repeated names accumulate
    span(name, fn) {
      const s = now(); const done = () => { const ms = now() - s; spans.push([name, ms]); };
      try { const r = fn(); if (r && typeof r.then === 'function') return r.finally(done); done(); return r; }
      catch (e) { done(); throw e; }
    },
    count(name, n = 1) { counts[name] = (counts[name] || 0) + n; },
    set(k, v) { tr.meta[k] = v; },
    flush(extra = {}) {
      if (process.env.PE_TRACE === '0') return;
      const phases = {};
      for (const [n, ms] of spans) phases[n] = +((phases[n] || 0) + ms).toFixed(2);
      const rec = { t: new Date().toISOString(), session: process.env.PE_SESSION || process.env.CLAUDE_SESSION_ID || '', cmd, total_ms: +(now() - t0).toFixed(1), phases, counts, ...tr.meta, ...extra };
      try { mkdirSync(dirname(RUNS), { recursive: true }); appendFileSync(RUNS, JSON.stringify(rec) + '\n'); } catch {}
      return rec;
    },
  };
  return tr;
}
// a no-op tracer, so library callers need not pass one
export const NOTRACE = { span: (n, f) => f(), count() {}, set() {}, flush() {} };

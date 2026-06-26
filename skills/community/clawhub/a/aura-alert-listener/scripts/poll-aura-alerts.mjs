#!/usr/bin/env node
/**
 * Aura Alert Listener — polls /v1/alerts every invocation.
 * Triggers an Agent Turn only when new actionable alerts exist.
 *
 * Exit 0 with no output = nothing to do (no LLM cost).
 * Exit 0 with JSON on stdout = actionable alerts found → Agent Turn.
 * Exit 1 = error (logged to stderr).
 * Exit 2 = missing config.
 */
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.env.AURA_BASE_URL || 'http://ryan-holmes-2.tail63f286.ts.net:8000';
const API_KEY = process.env.AURA_API_KEY;
const STATE_FILE = process.env.AURA_STATE_FILE || './memory/aura-alert-listener-state.json';
const ACK_PUSH = (process.env.AURA_ACK_PUSH || '1') === '1';

if (!API_KEY) {
  console.error('AURA_API_KEY is required');
  process.exit(2);
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(path.resolve(filePath)), { recursive: true });
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { checked_at: null, seen: {} };
  }
}

function saveState(state) {
  ensureDir(STATE_FILE);
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

const FETCH_TIMEOUT_MS = 15_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2_000;

async function jget(url, method = 'GET', attempt = 0) {
  try {
    const res = await fetch(url, {
      method,
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
    });

    const txt = await res.text();
    let body = {};
    try { body = txt ? JSON.parse(txt) : {}; } catch { body = { raw: txt }; }

    if (!res.ok) throw new Error(`${method} ${url} -> ${res.status} ${JSON.stringify(body)}`);
    return body;
  } catch (err) {
    if (attempt < MAX_RETRIES) {
      await new Promise(r => setTimeout(r, RETRY_DELAY_MS));
      return jget(url, method, attempt + 1);
    }
    throw err;
  }
}

function alertKey(a) {
  return (
    a?.data?.push_alert_id ||
    a?.data?.job_id ||
    a?.data?.task_id ||
    `${a?.type}|${a?.message}`
  );
}

function isActionable(a) {
  if (!a?.type) return false;
  if (a.type.startsWith('push.')) return true;
  return ['task.', 'job.', 'balance.low', 'policy.violation'].some(p => a.type.startsWith(p));
}

async function main() {
  const state = loadState();

  const [alertsResp, settings] = await Promise.all([
    jget(`${BASE}/v1/alerts`),
    jget(`${BASE}/v1/agents/settings`),
  ]);

  const alerts = alertsResp.alerts || [];
  const now = Math.floor(Date.now() / 1000);

  // Prune old seen keys (24h TTL)
  for (const [k, ts] of Object.entries(state.seen || {})) {
    if (now - Number(ts) > 86400) delete state.seen[k];
  }

  const fresh = [];
  for (const a of alerts) {
    const k = alertKey(a);
    if (!state.seen[k]) {
      state.seen[k] = now;
      fresh.push(a);
    }
  }

  const actionable = fresh.filter(isActionable);

  // Auto-ack push alerts
  if (ACK_PUSH) {
    for (const a of fresh) {
      if (a?.type?.startsWith('push.')) {
        const id = a?.data?.push_alert_id;
        if (id) {
          try { await jget(`${BASE}/v1/alerts/${id}/ack`, 'POST'); } catch {}
        }
      }
    }
  }

  if (alertsResp.checked_at) state.checked_at = alertsResp.checked_at;
  saveState(state);

  if (actionable.length === 0) {
    process.exit(0);
  }

  // Output actionable alerts for Agent Turn
  const out = {
    checked_at: alertsResp.checked_at || null,
    approval_mode: settings.approval_mode || 'auto',
    policy: settings.policy || null,
    actionable_count: actionable.length,
    alerts: actionable.map(a => ({
      type: a.type,
      priority: a.priority,
      message: a.message,
      data: a.data || {},
    })),
  };

  process.stdout.write(JSON.stringify(out));
}

main().catch(err => {
  console.error(String(err?.message || err));
  process.exit(1);
});

#!/usr/bin/env node
// PreToolUse hook for the Agent tool.
// Reads the hook event from stdin. A call with no model gets the default cheap
// model injected (updatedInput) and proceeds; nested spawns and calls over the
// per-session budget are denied with a reason. Every rule can be tuned with an
// environment variable — see README.md. Exit code is always 0: a hook that
// crashes must not block work.

'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');

const env = (name, fallback) => {
  const v = process.env[name];
  return v === undefined || v === '' ? fallback : v;
};

// Ordered cheapest → most expensive. These are also the only values the Agent
// tool's schema accepts for `model`, so only they may be injected.
const TIER_ORDER = ['haiku', 'sonnet', 'opus', 'fable'];
// A name that mentions several tiers resolves to the most expensive one, so the
// ceiling check errs on the side of blocking.
const tierOf = (model) => {
  if (typeof model !== 'string') return null;
  const m = model.toLowerCase();
  for (let i = TIER_ORDER.length - 1; i >= 0; i--) if (m.includes(TIER_ORDER[i])) return TIER_ORDER[i];
  return null;
};
const rank = (tier) => TIER_ORDER.indexOf(tier);

const out = (obj) => { process.stdout.write(JSON.stringify(obj)); process.exit(0); };
const deny = (reason) => out({
  hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: reason },
});

// Per-session state (spawn count, whether the user was told about the default)
// in the OS temp dir. Any failure → behave as if there were no state.
const STATE_TTL_MS = 7 * 24 * 60 * 60 * 1000;
const stateFile = (sessionId) => {
  const dir = path.join(os.tmpdir(), 'frugal-subagents');
  fs.mkdirSync(dir, { recursive: true });
  // Best-effort sweep of state files from sessions older than a week.
  try {
    const cutoff = Date.now() - STATE_TTL_MS;
    for (const f of fs.readdirSync(dir)) {
      const p = path.join(dir, f);
      try { if (fs.statSync(p).mtimeMs < cutoff) fs.unlinkSync(p); } catch { /* ignore */ }
    }
  } catch { /* ignore */ }
  return path.join(dir, `${String(sessionId).replace(/[^A-Za-z0-9_-]/g, '_')}.json`);
};
const loadState = (sessionId) => {
  if (!sessionId) return null;
  try { return { file: stateFile(sessionId), ...JSON.parse(fs.readFileSync(stateFile(sessionId), 'utf8')) }; }
  catch { try { return { file: stateFile(sessionId), count: 0, notified: false }; } catch { return null; } }
};
const saveState = (state) => {
  if (!state) return;
  try { fs.writeFileSync(state.file, JSON.stringify({ count: state.count, notified: state.notified, updated: Date.now() })); }
  catch { /* ignore */ }
};

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { raw += chunk; });
process.stdin.on('end', () => {
  let ev;
  try { ev = JSON.parse(raw); } catch { process.exit(0); }

  if (env('FRUGAL_SUBAGENTS_OFF', '0') === '1') process.exit(0);
  if (ev.hook_event_name !== 'PreToolUse') process.exit(0);
  if (!/^(Agent|Task)$/.test(String(ev.tool_name))) process.exit(0);

  const input = ev.tool_input || {};
  const explicit = typeof input.model === 'string' && input.model !== '' ? input.model : undefined;

  // 1. No subagents from inside a subagent. `agent_id` is present only when the
  //    hook fires inside a subagent's own session.
  if (ev.agent_id !== undefined && env('FRUGAL_SUBAGENTS_ALLOW_NESTED', '0') !== '1') {
    deny('frugal-subagents: nested subagents are blocked — this call comes from inside a subagent. '
      + 'Finish the task with your own tools and return the result to your caller; if the task '
      + 'genuinely needs a fleet, say so in your result instead of spawning. '
      + '(The user can lift this with FRUGAL_SUBAGENTS_ALLOW_NESTED=1.)');
  }

  // 2. Per-session spawn budget. Denied calls are not counted.
  const state = loadState(ev.session_id);
  const max = parseInt(env('FRUGAL_SUBAGENTS_MAX_SPAWNS', '12'), 10);
  if (state && Number.isFinite(max) && max > 0 && state.count + 1 > max) {
    deny(`frugal-subagents: this session has already spawned ${max} subagents (FRUGAL_SUBAGENTS_MAX_SPAWNS). `
      + 'Continue with the results you have, or send a follow-up to an agent that is still running '
      + 'instead of starting a new one; if more spawns are genuinely needed, ask the user to raise the limit.');
  }

  // 3. Model. Explicit wins; otherwise strict mode denies, default mode injects a cheap model.
  const ceiling = tierOf(env('FRUGAL_SUBAGENTS_MAX_TIER', ''));
  let model = explicit;
  let defaulted = false;
  if (!explicit) {
    if (env('FRUGAL_SUBAGENTS_REQUIRE_MODEL', '0') === '1') {
      deny('frugal-subagents: choose the model for this subagent explicitly (the "model" parameter). '
        + 'Web research, scanning, extraction and mechanical edits → "sonnet" or "haiku"; the '
        + 'session\'s top-tier model is justified only for judgment that cannot be delegated. '
        + 'Bundled workers: subagent_type "web-scout" (sonnet) and "extractor" (haiku). '
        + '(Strict mode — the user can switch it off with FRUGAL_SUBAGENTS_REQUIRE_MODEL=0.)');
    }
    let def = tierOf(env('FRUGAL_SUBAGENTS_DEFAULT_MODEL', 'sonnet')) || 'sonnet';
    if (ceiling && rank(def) > rank(ceiling)) def = ceiling;
    model = def;
    defaulted = true;
  } else if (ceiling && tierOf(explicit) && rank(tierOf(explicit)) > rank(ceiling)) {
    deny(`frugal-subagents: model "${explicit}" is above the ceiling "${ceiling}" configured for subagents `
      + `(FRUGAL_SUBAGENTS_MAX_TIER). Use "${ceiling}" or cheaper, or do this part in the main session.`);
  }

  // Allowed: count it, then either pass through untouched or inject the default.
  if (state) { state.count += 1; }
  if (!defaulted) { saveState(state); process.exit(0); }

  // "allow" alongside updatedInput mirrors the documented shape and removes any
  // doubt about whether a bare updatedInput is applied; the Agent tool itself
  // doesn't prompt for permission, so nothing is bypassed.
  const result = {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'allow',
      updatedInput: { ...input, model },
      additionalContext: `frugal-subagents: this subagent runs on "${model}" because no model was named. `
        + 'Name the model explicitly when a different tier is justified.',
    },
  };
  if (state && !state.notified) {
    state.notified = true;
    result.systemMessage = `frugal-subagents: subagents spawned without an explicit model run on "${model}" `
      + '(FRUGAL_SUBAGENTS_DEFAULT_MODEL). Nested spawns are blocked; '
      + `budget ${Number.isFinite(max) && max > 0 ? max : 'unlimited'} spawns per session.`;
  }
  saveState(state);
  out(result);
});

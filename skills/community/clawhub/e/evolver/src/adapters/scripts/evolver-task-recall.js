#!/usr/bin/env node
// evolver-task-recall.js
// UserPromptSubmit hook: on each user prompt, find GEP assets (Hub genes +
// local genes) that match the task and inject a distilled hint so a GENERAL
// agent benefits from prior distilled capabilities without manually calling
// MCP tools. This is the per-harness shell around src/gep/recallInject.js.
//
// Input  (stdin JSON, Claude Code UserPromptSubmit):
//   { "prompt": "...", "session_id", "cwd", "transcript_path", ... }
// Output (stdout JSON, exit 0 ALWAYS):
//   enforce + match -> { agent_message, additionalContext,
//                        hookSpecificOutput: { hookEventName, additionalContext } }
//   everything else -> {}   (injects nothing)
//
// DESIGN CONTRACT (the fail-open core — see also recallInject.js invariants):
//   - DEFAULT off. off finishes {} WITHOUT parsing the prompt body.
//   - shadow computes + logs what WOULD inject but injects nothing.
//   - enforce injects the distilled hint.
//   - FAIL-OPEN: any error/timeout/empty -> exactly one finish({}). The hook
//     blocks the user's prompt, so it must NEVER hang or crash the session.
//     Claude Code's timeout fail-open behaviour is UNDOCUMENTED, so we own the
//     deadline ourselves with a single watchdog + latch (never rely on the
//     host to kill us gracefully).
//   - STDOUT is a single JSON object. Any stray console.log() from a
//     transitively-required module (e.g. signals._mergeSignals, hubSearch
//     fetch-cost log, assetStore seeding) would corrupt it — so we redirect
//     console.* to stderr before requiring anything heavy.

'use strict';

// --- stdout-poison defense: route all console.* to stderr ------------------
// Modules we require (hubSearch, signals, assetStore, …) call console.log,
// which writes to stdout. The hook contract is ONE JSON object on stdout, so
// we redirect every console method to stderr. stderr on exit 0 is not fed to
// the model for UserPromptSubmit; on non-2 exit only its first line shows in
// the transcript as a hook-error notice — acceptable and we exit 0 anyway.
for (const m of ['log', 'info', 'warn', 'error', 'debug']) {
  try { console[m] = function () { try { process.stderr.write(''); } catch (_) {} }; } catch (_) {}
}

const path = require('path');

// ---- Timing budget, coherent with the host kill ---------------------------
// The host (Claude Code) kills this process at the hook's `timeout` (5s in
// buildClaudeHooks -> 5000ms). Our OWN absolute watchdog MUST fire comfortably
// BEFORE that, or the host could kill us mid-write and break the fail-open
// stdout contract. So:
//   ABSOLUTE_DEADLINE_MS (3300) < host 5000ms  -> ~1.7s headroom for finish().
// EVOLVER_RECALL_TIMEOUT_MS is the Hub SEARCH budget only (clamped well under
// the absolute deadline). The actual budget handed to the search is computed
// DYNAMICALLY at search-start as (deadline - already-elapsed - safety), so
// slow stdin/require can never let the search run past the watchdog (which
// would otherwise spuriously return {} — Bugbot #183 medium findings).
const T0 = Date.now();
const ABSOLUTE_DEADLINE_MS = 3300;   // watchdog; strictly < host timeout (5000ms)
const SEARCH_SAFETY_MS = 250;        // leave room for finish() after the search
const MIN_SEARCH_MS = 300;           // below this, skip the search (finish {})

function getSearchBudgetMs() {
  const n = parseInt(process.env.EVOLVER_RECALL_TIMEOUT_MS, 10);
  // Hard cap at 2800 so even a max-budget search starts and ends before the
  // 3300ms watchdog under any realistic startup cost.
  return Number.isFinite(n) && n >= 500 && n <= 2800 ? n : 2000;
}

function getMode() {
  const v = String(process.env.EVOLVER_RECALL_MODE || '').toLowerCase().trim();
  return v === 'shadow' || v === 'enforce' ? v : 'off';
}

let handled = false;
let watchdog = null;

// Single-writer latch: exactly one stdout write, exactly one exit. Mirrors the
// proven pattern in evolver-signal-detect.js / evolver-session-end.js.
function finish(obj) {
  if (handled) return;
  handled = true;
  if (watchdog) { try { clearTimeout(watchdog); } catch (_) {} }
  try { process.stdout.write(JSON.stringify(obj || {})); } catch (_) {}
  process.exit(0);
}

function main() {
  const mode = getMode();

  // Absolute watchdog, armed at process entry and INDEPENDENT of the search
  // budget. Fires at ABSOLUTE_DEADLINE_MS (3300ms) — strictly under the host's
  // timeout (5000ms) so the host can never kill us mid-write. If stdin never
  // closes OR anything hangs, we emit {} and exit cleanly first.
  watchdog = setTimeout(() => finish({}), ABSOLUTE_DEADLINE_MS);

  let buf = '';
  try {
    process.stdin.setEncoding('utf8');
  } catch (_) { /* some hosts pass no stdin */ }
  process.stdin.on('data', (c) => { buf += c; });
  process.stdin.on('error', () => finish({}));
  process.stdin.on('end', () => {
    if (handled) return;

    // off: do NOT even parse the prompt body (privacy: nothing read/sent).
    if (mode === 'off') return finish({});

    let prompt = '';
    let sessionId = '';
    try {
      const input = buf.trim() ? JSON.parse(buf) : {};
      prompt = String(input.prompt || '').trim();
      sessionId = String(input.session_id || input.sessionId || '').trim();
    } catch (_) {
      return finish({});
    }
    if (prompt.length < 8) return finish({}); // trivial prompt -> skip

    // Heavy require INSIDE try/catch: a broken require graph must fail open,
    // not crash the user's prompt (this is also why the e2e test runs the
    // copied hook with mode=off and asserts exit 0 + parseable stdout).
    let core;
    try {
      const { findEvolverRoot } = require('./_runtimePaths');
      const root = findEvolverRoot();
      if (!root) return finish({});
      core = require(path.join(root, 'src', 'gep', 'recallInject.js'));
    } catch (_) {
      return finish({});
    }

    // Pass the ABSOLUTE deadline (T0 + watchdog window) plus the configured
    // search cap. The core bounds the Hub call by the time REMAINING to that
    // deadline (minus its own post-await safety margin) and runs local-gene
    // disk I/O BEFORE the Hub await — so neither the Hub search nor the
    // post-processing can overrun the watchdog (Bugbot #183: slow startup or a
    // budget-eating Hub call must not let the timer fire mid-work). If too
    // little time remains even before starting, skip and fail open.
    const elapsed = Date.now() - T0;
    const remaining = ABSOLUTE_DEADLINE_MS - elapsed - SEARCH_SAFETY_MS;
    if (remaining < MIN_SEARCH_MS) return finish({});
    const deadlineMs = T0 + ABSOLUTE_DEADLINE_MS;

    Promise.resolve()
      .then(() => core.recallForTask({ prompt, mode, sessionId, timeoutMs: getSearchBudgetMs(), deadlineMs }))
      .then((r) => {
        if (r && r.inject && r.text) {
          // Emit BOTH shapes:
          //   - nested hookSpecificOutput.additionalContext is the DOCUMENTED
          //     canonical UserPromptSubmit injection shape (system-reminder,
          //     no transcript noise).
          //   - flat additionalContext / agent_message match the in-repo
          //     precedent (session-start.js) for hosts that read the flat key.
          // Extra keys are tolerated/ignored by hosts; whichever wins, the
          // other is harmless.
          return finish({
            agent_message: r.text,
            additionalContext: r.text,
            hookSpecificOutput: {
              hookEventName: 'UserPromptSubmit',
              additionalContext: r.text,
            },
          });
        }
        // shadow (logged inside the core) and no-match both inject nothing.
        return finish({});
      })
      .catch(() => finish({}));
  });
}

if (require.main === module) {
  main();
} else {
  module.exports = { getMode, getSearchBudgetMs };
}

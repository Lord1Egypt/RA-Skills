"use strict";

/**
 * First-run prompt that introduces the ATP autoBuyer to interactive users.
 *
 * Triggers when ALL conditions hold:
 *   - process.stdin.isTTY === true (skipped under systemd, Docker, CI)
 *   - EVOLVER_ATP_AUTOBUY is not already set (neither on nor off)
 *   - ack file memory/atp-autobuy-ack.json does not exist (already decided)
 *
 * Outcomes:
 *   - user answers y         -> autoBuyer.setConsent(true) — opts in for future sessions
 *   - user answers n         -> autoBuyer.setConsent(false) — prompt never shown again
 *   - user answers later     -> no ack written, prompt shown next session
 *   - any non-TTY/ack branch -> silent no-op
 *
 * setConsent failures (FS permission, disk full) are surfaced to the user
 * via the output stream and returned as `reason: 'ack_write_failed'`; the
 * decision field still reflects what the user typed.
 */

const readline = require("readline");
const autoBuyer = require("./autoBuyer");

// All ack file plumbing lives on autoBuyer (filename constant, path
// resolution, read with strict validation, atomic write via tmp+rename).
// cliAutobuyPrompt always reaches it through the public surface so the
// two modules cannot diverge on schema or validation — pre-consolidation
// drift bit us twice (Bugbot PR #141: duplicate writers + lenient-vs-
// strict reader). No __internals re-export here either: tests import
// autoBuyer directly so a future rename trips a single set of asserts.

/**
 * @returns {"ack_present"|"env_set"|"non_tty"|"eligible"}
 */
function classify(env, stdin) {
  const envVal = env && env.EVOLVER_ATP_AUTOBUY;
  if (typeof envVal === "string" && envVal.trim().length > 0) {
    return "env_set";
  }
  if (!stdin || !stdin.isTTY) {
    return "non_tty";
  }
  if (autoBuyer.readAck()) {
    return "ack_present";
  }
  return "eligible";
}

function _ask(question, { input, output }) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input, output });
    rl.question(question, (answer) => {
      rl.close();
      resolve((answer || "").trim().toLowerCase());
    });
  });
}

/**
 * Synchronously decide whether to prompt (TTY + no ack + env unset) and,
 * if prompting, block on user answer. Resolves with:
 *   { prompted: bool, decision: "yes"|"no"|"later"|null, reason: string }
 *
 * Should be called at most once per `evolver run` invocation, BEFORE the
 * autoBuyer.start() branch in the run loop.
 *
 * @param {object} [opts]
 * @param {NodeJS.ReadableStream} [opts.input]
 * @param {NodeJS.WritableStream} [opts.output]
 * @param {NodeJS.ProcessEnv} [opts.env]
 * @param {(q: string, io: object) => Promise<string>} [opts.ask]
 * @returns {Promise<{ prompted: boolean, decision: string|null, reason: string }>}
 */
async function runPrompt(opts) {
  opts = opts || {};
  const input = opts.input || process.stdin;
  const output = opts.output || process.stdout;
  const env = opts.env || process.env;
  const ask = typeof opts.ask === "function" ? opts.ask : _ask;

  const state = classify(env, input);
  if (state !== "eligible") {
    return { prompted: false, decision: null, reason: state };
  }

  try {
    output.write("\n");
    output.write("[ATP-AutoBuyer] Your evolver will automatically place small-priced\n");
    output.write("ATP orders when it detects a capability gap. This spends real\n");
    output.write("credits on the EvoMap hub and is ON by default for new installs.\n");
    output.write("  - daily hard cap:   ATP_AUTOBUY_DAILY_CAP_CREDITS (default 50)\n");
    output.write("  - per-order cap:    ATP_AUTOBUY_PER_ORDER_CAP_CREDITS (default 10)\n");
    output.write("  - change later:     evolver atp enable | evolver atp disable\n");
    output.write("\n");
  } catch (_) {
    return { prompted: false, decision: null, reason: "io_error" };
  }

  let answer;
  try {
    answer = await ask("Keep ATP auto-spend ON for future sessions? [y=keep enabled / n=disable / later=ask again next session] ", {
      input,
      output,
    });
  } catch (_) {
    return { prompted: true, decision: null, reason: "ask_error" };
  }

  // For y/n we persist via autoBuyer.setConsent (atomic tmp+rename, throws
  // on FS failure). If the write fails we MUST tell the user — for the 'n'
  // path especially, since auto-spend is default-ON and a failed disable
  // means the user typed "off" but the runtime keeps charging credits
  // (Bugbot PR #141 Medium: unchecked ack write). Do NOT mutate process.env
  // on success: that would double-signal and shadow any explicit operator
  // preference set later.
  function _persistConsent(enabled, decision) {
    try {
      autoBuyer.setConsent(enabled);
      return { prompted: true, decision, reason: enabled ? "user_accepted" : "user_declined" };
    } catch (err) {
      try {
        output.write("[ATP-AutoBuyer] WARN: failed to persist consent: " + (err && err.message || err) + "\n");
        if (enabled) {
          output.write("                Auto-spend will keep using the default-on policy until\n");
          output.write("                the ack is saved (capped at the configured caps).\n");
        } else {
          output.write("                Auto-spend will STAY ON (default policy) until your opt-out\n");
          output.write("                can be saved — your decline was not persisted.\n");
        }
        output.write("                Check disk space and write permissions on the memory dir, then run\n");
        output.write("                `evolver atp " + (enabled ? "enable" : "disable") + "` to retry.\n");
      } catch (_) { /* output stream is broken too — nothing more we can do */ }
      return { prompted: true, decision, reason: "ack_write_failed" };
    }
  }

  if (answer === "y" || answer === "yes") {
    return _persistConsent(true, "yes");
  }
  if (answer === "n" || answer === "no") {
    return _persistConsent(false, "no");
  }
  // Postpone: no ack written, so autoBuyer.getConsent() returns
  // {enabled: true, source: 'default'} this session. Auto-spend keeps
  // running under the default policy with caps; the prompt will fire again
  // next interactive session so the user can confirm or opt out.
  return { prompted: true, decision: "later", reason: "user_postponed" };
}

module.exports = {
  runPrompt,
  classify,
};

/**
 * Collect call recordings into the cadence layer.
 *
 * The deterministic half of call capture: it pulls every call held in a
 * rolling window whose transcript the recorder has finished processing, and
 * writes one raw file per call under `cadence/log/raw/calls/`. It makes no
 * judgements — no summary, no intel, no context. That is the scribe agent's
 * job, and keeping the two apart is the point: a fetch loop an LLM re-derives
 * every morning is a fetch loop that silently changes shape.
 *
 * Run from the repo root:
 *
 *   npx tsx scripts/call-capture/collect/calls.ts --list
 *   CALL_RECORDER_API_KEY=… npx tsx scripts/call-capture/collect/calls.ts --dry-run
 *   CALL_RECORDER_API_KEY=… npx tsx scripts/call-capture/collect/calls.ts
 *
 * `--list` prints the recorders that ship and what each wants for a
 * credential. `--recorder=<slug>` overrides `config.ts` for one run.
 *
 * The assignment above is only for a run by hand: deployed, the key comes from
 * the workspace environment variables a harness agent inherits.
 *
 * Idempotent. A call already present anywhere under `cadence/log/` — raw or
 * long since scribed — is skipped, so re-running costs nothing and the
 * overlapping window is free. Note that the key includes the recorder slug: a
 * switch of recorder is a switch of id space, and history captured under the
 * old one reads as uncaptured.
 *
 * This file is the wiring and nothing else. `recorder.ts` holds the contract
 * and everything that is true whoever records your calls; `recorders/` holds
 * one adapter per vendor and the registry that names them. To support a
 * recorder that is not there, write an adapter beside the others and register
 * it — see `references/providers.md`.
 */
import { capture, checkFlags, ConfigError } from "./recorder";
import { recorderTable, resolve } from "./recorders";

try {
  const argv = process.argv.slice(2);
  checkFlags(argv);

  if (argv.includes("--list")) {
    console.log(recorderTable());
  } else {
    const { recorder, entry } = resolve(argv);
    if (entry.written === "docs") {
      console.error(
        `note: the ${entry.label} adapter was written from vendor docs and not ` +
          `yet run against a live workspace. Check --dry-run lists real calls ` +
          `before trusting a clean run.`,
      );
    }
    await capture(recorder);
  }
} catch (error) {
  // A configuration error is a message, not a stack trace: the reader needs
  // to know which variable to set, not which line threw.
  if (error instanceof ConfigError) {
    console.error(error.message);
    process.exit(1);
  }
  throw error;
}

import { defineAgent } from "@cargo-ai/cdk";

import { callScribePrompt } from "./call-scribe.prompt";
import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";

// The scribe: a Claude Code harness agent, not a streamText agent.
//
// `harnessSlug: "claudeCode"` swaps the LLM loop for the coding runtime, and
// that is what makes this skill possible. The output of a call is not a column
// value; it is a diff across the repo — a raw capture, a log entry, an
// objection file that just gained its second occurrence. Only an agent with a
// working tree can produce one, and only a pull request makes it reviewable
// before it becomes what every other agent believes.
//
// `connector` and `languageModel` are required even here. The harness does not
// bring its own model: it runs against Cargo's LLM proxy, which bills this
// connector and meters usage against this slug. Any Anthropic model works with
// `claudeCode`; see `../connectors/anthropic.ts`.
//
// This replaces a scheduled CI workflow that launched a hosted agent. One
// resource now holds the schedule, the repository binding and the
// instructions, declared in the same project as everything else the workspace
// runs.
export const callScribe = defineAgent("call_scribe", {
  name: "Call scribe",
  description:
    "Collects yesterday's call recordings into the cadence layer, scribes them, and opens one reviewable pull request.",
  color: "blue",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER — your model of choice
  // No `state`, and nothing to put in one. Deploy binds this project's
  // connected state (cargo.state.json) and the harness clones its repository
  // at the state's directory and production branch — which is the correct
  // binding, not a shortcut: the repository holding cadence/ and context/ IS
  // this project's. Name another project with `stateRef(uuid)` only to
  // override that. `cargo-ai project check` prints the binding; the state's
  // directory must be where the agent's `npx tsx` resolves node_modules from,
  // and a project whose state is not connected deploys this agent unbound.
  //
  // No `env` either. The recorder and the internal domain are in
  // scripts/call-capture/collect/config.ts, where the compiler checks the slug
  // and the harness picks up an edit on its next clone. CALL_RECORDER_API_KEY
  // is a workspace environment variable the harness inherits:
  //
  //   export CALL_RECORDER_API_KEY=…   # not committed, not persisted
  //   cargo-ai workspaceManagement envVar create \
  //     --key CALL_RECORDER_API_KEY --secret
  //
  // Not `secret()`, which would resolve from the deploying machine and need
  // the key exported for every deploy. `references/providers.md` has the rest,
  // including the `<key>:<secret>` form Gong and Clari Copilot need.
  triggers: [
    {
      type: "cron",
      name: "daily",
      // 07:00 UTC: after the recorder has finished processing yesterday's
      // calls, before anyone reads the repo in the morning. Anything still
      // processing at this minute is picked up by tomorrow's run, which is why
      // the collector's window is three days wide and not one.
      cron: "0 7 * * *",
      text: "Run the daily call capture. Follow your system prompt exactly and open one pull request.",
    },
  ],
  systemPrompt: callScribePrompt,
  folder: agentsFolder,
});

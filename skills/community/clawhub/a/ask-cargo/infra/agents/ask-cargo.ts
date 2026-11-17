import { agentConnectorTrigger, defineAgent } from "@cargo-ai/cdk";

import { askCargoPrompt } from "./ask-cargo.prompt";
import { anthropic } from "../connectors/anthropic";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { askCargoUser } from "../users";

// Ask Cargo: one agent the whole team @mentions in Slack, sitting on top of the
// GTM repository and the workspace it deploys.
//
// `harness: "claudeCode"`, not a streamText agent, because the answers people
// need most are in the repo — the ICP in context/, what last week looked like
// in cadence/, what is actually declared in infra/ — and the changes they ask
// for are diffs. Only an agent with a working tree can read all of that at
// once and turn "add Ramp to the competitor list" into a pull request. The
// workspace's built-in Master Agent already answers from context and models
// without a checkout; this one exists for everything that needs the repo.
//
// `connector` and `languageModel` are required even here. The harness does not
// bring its own model: it runs against Cargo's LLM proxy, which bills this
// connector and meters usage against this slug. Any Anthropic model works with
// `claudeCode`; see `../connectors/anthropic.ts`.
//
// No `uses`, on purpose. The Slack trigger replies in the thread by itself,
// so there is no postMessage to declare. Handing work to other agents — the
// standup, the weekly planner, the account scorer — goes through
// `cargo-ai ai message create` from the sandbox, not through `uses`: a handle
// in `uses` would import another cookbook's file, which is exactly the
// cross-folder import this repo refuses, and it would freeze the roster at
// deploy time. The CLI reads whatever agents the workspace has today.
//
// No `capabilities`, for the same reason standup has none: the workspace is
// read with Cargo's own CLI, which the harness already has, and only the
// prompt can say which commands need a "go" in the thread first. The rules
// are in `ask-cargo.prompt.ts`. The CLI is signed in as the `ask_cargo`
// service user (`runAs`), a viewer: see `../users`.
export const askCargo = defineAgent("ask_cargo", {
  name: "Ask Cargo",
  description:
    "The team's GTM agent in Slack: answers from the repo and the workspace, opens pull requests for changes, and hands work to the other agents only after a go in the thread.",
  color: "blue",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER — your model of choice
  // No `state`: deploy binds this project's connected state (the one
  // cargo.state.json points at), and the harness clones its repository at the
  // state's directory and production branch. `cargo-ai project check` prints
  // the binding. A project whose state is not connected deploys this agent
  // unbound, with an empty sandbox and the plan note `unbound: this project's
  // state is not connected`; connect the project before relying on it.
  //
  // No `env` either: the one value a reply needs — the bot's own mention, so
  // it can say what to type to confirm — arrives in every message that wakes
  // the agent as Slack's raw `<@U…>` token, which the prompt reuses.
  runAs: askCargoUser,
  triggers: [
    agentConnectorTrigger({
      connector: slack,
      config: {
        // Every channel the bot is in, so `@Cargo` works wherever the team
        // already talks, with no list to keep in sync. It is the workspace
        // default, not an override: a channel another agent lists is left to
        // that agent, so a dedicated bot (a standup channel, a deal room)
        // still owns its own channel. Direct messages are not included.
        //
        // The boundary moves from this file to Slack: the agent answers in
        // any channel the bot has been invited to, customer shared channels
        // included. Keep the bot out of those, or list them on another agent.
        allChannels: true,
      },
    }),
  ],
  systemPrompt: askCargoPrompt,
  folder: agentsFolder,
});

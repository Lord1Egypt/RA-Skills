# Ask Cargo: ask your go-to-market repo and workspace anything from Slack

To give the whole team one place to ask about the go-to-market stack, deploy one agent they @mention
in Slack, on top of your repository and the workspace it deploys. It answers from what is written
and what actually ran, turns change requests into pull requests, and hands work to the agents that
own it only after someone in the thread says go. A Claude Code harness agent with a Slack connector
trigger; nothing else is deployed.

```sh
cargo-ai project add cookbook/ask-cargo
```

## What it does

- **Answers.** Reads `context/`, `cadence/`, `infra/` and read-only `cargo-ai` calls (runs, batches,
  usage, what is deployed), and cites the file or command behind every answer.
- **Changes.** Edits the repository on a branch and replies with the pull request. One thread is one
  pull request; a follow-up adds a commit. It never merges and never deploys.
- **Runs, on a go.** Proposes what will run, over how many records, at the live price, and waits for
  `@Cargo go` in the thread. Batches over 25 records run a sample of 5 first.
- **Captures.** "@Cargo capture this" turns the thread into a raw capture and a log entry under
  `cadence/log/slack/`, and promotes a claim into `context/` only once it repeats across calls and
  threads, on the thread's pull request. It reads only that thread (`getThread`), and refuses shared
  channels and DMs.
- **Hands off.** When a deployed agent owns the job (standup, weekly planning, the account scorer), it
  messages that agent with `cargo-ai ai message create` instead of redoing the work.

## How it works

1. **Someone @mentions the bot** in any channel it is in. The Slack trigger opens one chat per thread
   (keyed on the channel and the thread's first message) and marks the thread "is working…".
2. **The harness clones the repository**, resolved from the checkout's git origin at deploy.
3. **The agent reads**, then either answers, opens or updates the thread's pull request, or replies
   with a proposal ending in the exact text to type to approve it.
4. **The platform streams the final text into the thread.** The agent posts nothing itself.
5. **A follow-up @mention in the same thread** lands in the same chat, so the agent sees its own
   proposal and the go together.

Adds 5 resources.

| File                               | Resource                        | Role                                                         |
| ---------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| `infra/agents/ask-cargo.ts`        | `defineAgent` (claudeCode)      | the Slack trigger, repository binding, model                 |
| `infra/agents/ask-cargo.prompt.ts` | (not a resource)                | the rules: what it reads, changes, and waits for a go on     |
| `infra/connectors/slack.ts`        | `defineConnector` (`slack`)     | the trigger; the platform replies through it                 |
| `infra/connectors/git.ts`          | `defineConnector` (`github`)    | the clone, branch, push and pull request path                |
| `infra/connectors/anthropic.ts`    | `defineConnector` (`anthropic`) | the model the harness runs on, billed and metered            |
| `infra/folders/index.ts`           | `defineFolder`                  | the workspace folder this cookbook's agent is filed in       |
| `infra/users/index.ts`             | `defineUser`, `defineRole`      | the viewer service user every turn's `cargo-ai` runs as      |
| `references/roster.md`             | (not a resource)                | which deployed agent owns which job                          |
| `references/capture-entry.md`      | (not a resource)                | what a capture writes, and how a re-mention is handled       |

## Why a trigger and not a Slack bot

A Slack connector trigger already is the bot. It acknowledges Slack inside the three-second window,
de-duplicates retries, keeps one chat per thread, shows a working status, streams the answer back,
and gives the thread a stop button. Everything a hand-built bot would need a worker, a token and a
queue for is platform behaviour here. The cost is what the trigger does not do, and the design is
shaped around those gaps:

- **Only @mentions wake it**, follow-ups included, and a mention sent mid-turn is dropped. So the
  confirmation is itself a mention (`@Cargo go`), and every reply that needs one says so.
- **The model is not told who wrote a message.** Multiplayer means anyone in the thread can steer
  and approve; it does not mean the agent knows who they are. Pull requests quote the request and
  name no one.
- **The trigger adds Slack tools with no channel lock** (`postMessage`, history, thread, reactions).
  The prompt forbids them, except reading and reacting to the summoning thread during a capture: a
  new chat only receives the mention and the thread's first message, so a capture has to read the
  replies itself. The reply is still the final text, in the thread it was asked in.

## Why the CLI for handoffs, not `uses`

`uses` accepts other agents, and a sub-agent there would be the obvious way to build an
orchestrator. It is the wrong one here for two reasons. A handle on `uses` imports another cookbook's
file, which breaks the isolation that lets a customer install exactly one cookbook. And it freezes
the roster at deploy: the agent could only reach the agents that existed when it shipped. From the
sandbox, `cargo-ai ai agent list` sees what the workspace runs today, and `ai message create` sits
behind the same go as every other action, which a sub-agent tool call would skip.

## Why not the built-in Master Agent

Workspaces ship a read-only Master Agent that answers from context and models and can run actions.
If that is all the team needs, put a Slack trigger on it and skip this cookbook (`master-agent-slack`
in `SKILL.md`). Ask Cargo is for what needs a checkout: reading what is declared in `infra/`,
answering from the cadence log, and turning a Slack message into a diff someone reviews.

## Placeholders (edit before deploy)

1. **Where the bot is** — the trigger is `allChannels`, so the agent answers in every channel the
   bot has been invited to. Keep it out of customer shared channels, or switch to `channelIds`.
2. **`languageModel`** — `infra/agents/ask-cargo.ts`: any Anthropic model the workspace's connector
   can reach.
3. **`references/roster.md`** — the agents your workspace runs, from `cargo-ai ai agent list`.

## What it does not do

It does not deploy, merge, destroy or remove anything, mint tokens, change members, post to any
channel but the thread it was asked in, send to people the workspace has no consent basis for, or
run anything that spends without a go in the thread.

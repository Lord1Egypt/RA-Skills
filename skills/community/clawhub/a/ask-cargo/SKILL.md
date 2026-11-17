---
name: ask-cargo
description: 'Ask your go-to-market repo and workspace anything from Slack: one agent the whole team @mentions answers from context, cadence and live runs, turns change requests into pull requests, captures a thread worth keeping into the cadence log and context, and hands work to the other deployed agents only after a go in the thread. Triggers: "let the team ask our GTM agent from slack", "one agent on top of all the others", "a slack bot that knows our repo", "ask cargo from slack", "orchestrator agent for our GTM stack", "let anyone open a PR from slack", "capture this slack thread into our context". Cargo project, defineAgent, harness claudeCode, Slack connector trigger, GitHub, cargo-ai CLI. Skip when: you want the day recapped and posted to Slack on a schedule, which is standup; or you want an answer in this chat right now with nothing deployed.'
version: "0.3.0"
compatibility: "Requires @cargo-ai/cli 1.0.154 or later with @cargo-ai/cdk 1.0.150 or later, which binds a harness agent to the project's connected state and takes `runAs` at the top level of `defineAgent`. Also needs a Cargo workspace, an authenticated LLM connector (the harness runs against Cargo's proxy), a GTM repository (the shape `cargo-ai project init` scaffolds), and authorized GitHub and Slack connectors."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/ask-cargo
metadata:
  author: getcargo
  source: cookbook
  personas:
    - revops
    - sales-leadership
    - gtm-engineering
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Ask Cargo

## The outcome

Anyone on the team types `@Cargo` in a Slack channel and gets the agent that knows the whole GTM
repo and the workspace behind it. One thread is one conversation, and anyone in the thread can steer
it. Four kinds of request land:

1. **Questions.** "What is our ICP for fintech?", "did the scorer run last night?", "what did we
   spend on enrichment this week?". It answers from `context/`, `cadence/`, `infra/` and read-only
   `cargo-ai` calls, and cites the file or the command.
2. **Changes.** "Add Ramp to our competitors", "tighten the disqualifiers". It makes the edit on a
   branch and replies with a pull request. One thread, one pull request; a follow-up in the thread
   is another commit on it. It never merges and never deploys.
3. **Work.** "Re-score Acme", "run the weekly plan now", "enrich these five domains". It proposes
   what will run, over how many records, at what live price, and does nothing until someone replies
   `@Cargo go`. When a deployed agent owns the job (the scorer, the planner, the standup) it hands
   the request to that agent with `cargo-ai ai message create` instead of redoing it.
4. **Captures.** "@Cargo capture this" in a thread worth keeping (what a customer said, a deal
   decision, a competitor sighting). It reads that one thread, writes a raw capture and a log entry
   under `cadence/log/slack/`, and promotes a claim into `context/` only once it repeats across
   calls and threads, on the thread's pull request. Shared channels and DMs are refused.
   `references/capture-entry.md` is the shape. The thread's channel id and parent ts come from the
   first line of the message the Slack trigger delivers (`[Slack channel: … | thread ts: … |
   message ts: …]`); if that line is missing, the agent asks once for the thread's permalink and
   stops.

This is not the workspace's built-in Master Agent. That one answers from context and models with no
checkout and cannot change anything. Ask Cargo exists for what needs the repository: reading what is
declared, and turning a Slack message into a reviewable diff. The resources are in
`infra/ask-cargo/agents/ask-cargo.ts` and the rules beside it in `ask-cargo.prompt.ts`.

How Slack reaches it, which shapes the rules (verified against the platform, not assumed):

- **Only @mentions wake it**, in any channel the bot is in, including follow-ups in a thread it already
  answered. A mention sent while it is still working is dropped, not queued. So every reply that
  needs an answer says exactly what to type next.
- **The platform posts the reply.** The agent's final text streams into the thread. There is no
  `postMessage` on the agent, and the prompt forbids the Slack tools the trigger adds on its own,
  except `getThread`, `listUsers` and `addReaction` on the summoning thread during a capture: a new
  chat receives only the mention and the thread's first message, not the replies in between.
- **It does not know who wrote a message.** The Slack user id stays in trigger metadata the model
  never sees, so a pull request quotes the request and does not name the requester.

## Example

> Put one agent in our #gtm Slack channel that answers from this repo, opens a pull request for any edit, and runs nothing until someone says go.

Illustrative output, fictional records:

```text
#gtm
Dana:   @Cargo add Globex to our competitors, they keep showing up in fintech deals
Cargo:  Opened https://github.com/northwind-example/gtm/pull/212 on branch ask-cargo/add-globex-competitor.
        • Adds Globex to context/ competitors with the fintech positioning from this thread
        • `cargo-ai project check` passes; nothing under infra/ changed
        Want a battlecard section too? Reply @Cargo with what to add.
Dana:   @Cargo also note they undercut on price for teams under 50 seats
Cargo:  Pushed a second commit to the same pull request (#212): pricing note added.
        Review and merge it when it reads right; I never merge.
```

One thread became one reviewable pull request with two commits; a request that spends, such as
re-scoring an account, would instead get a proposal with its live price and wait for `@Cargo go`.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not,
this is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/ask-cargo` writes this example to `infra/ask-cargo/` and this
   procedure to `.agents/skills/ask-cargo/`. No project yet?
   `cargo-ai project init <dir> --cookbook ask-cargo && cd <dir> && npm install` does both; this
   folder never ships a shell. **If you are reading this from the project's `.claude/skills/`, the
   install already happened — start at step 2.** On a CLI too old to have `add`, copy this folder in
   as a sibling of what is there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has a GitHub, Slack or
   Anthropic connector (standup and weekly-planning each bring one), rewire the imports to the
   existing one and drop the copy; two resources with one slug is a collision at deploy.
3. **Check where the bot already is.** Authorize the Slack connector if the workspace does not have
   one (`cargo-ai project add connector/slack`). The trigger is `allChannels`, so the agent answers in
   every channel the bot has been invited to: list them from the connector's channel autocomplete
   and flag any customer shared (Slack Connect) channel before deploying.
4. **Write the roster.** Fill `references/roster.md` from `cargo-ai ai agent list`: which deployed
   agent owns which job. The prompt reads it from the installed skill folder.
5. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted; _What you will be asked_ is the floor, and you derive before you ask. Record
   what you changed and why under a `## Decisions` section in your copy of this file.
6. **Plan, then stop.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root, show the diff, and deploy only on an explicit yes: `cargo-ai project deploy`. Never
   `cargo-ai project init --force` into a non-empty directory.
7. **Verify.** Walk _Done when_ line by line and report each with evidence. Read out loud the
   channels the bot is in before you call this done: a customer shared channel among them is the
   failure nobody can undo.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked.

| Input                                                     | Kind  | How it is answered                                                                                                                                                                                                                                                | Why it matters                                                                                                                                                                                                                  |
| --------------------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project binding (`infra/agents/ask-cargo.ts`) | value | **derived**: leave `state` unset and deploy binds the project's connected state (`cargo.state.json`): its repository, directory and production branch. `cargo-ai project check` prints the binding; a project whose state is not connected deploys the agent unbound, with an empty sandbox.                               | This is the checkout every answer reads and every pull request opens against. An `owner/name` typed by hand is the value nobody notices is wrong until a pull request lands on a stranger's repository.                         |
| service user (`infra/users/index.ts`)                     | value | **derived**: `ask_cargo`, a service user on the adopted `viewer` system role. Deploying creates it; the deploying user's own role must cover viewer.                                                                                                               | Every turn's `cargo-ai` session. Viewer reads runs, models, agents and usage and can message other agents, but cannot deploy or change a resource, so the prompt's limits hold even when the prompt is ignored.               |
| Slack, GitHub and LLM connectors (`infra/connectors/`)    | value | **derived**: `cargo-ai connection connector list` shows what is authorized; `cargo-ai project add connector/<slack\|github\|anthropic>` opens the consent for what is missing. All three are `default: true` because a deploy cannot mint a grant.                      | Slack is the trigger, GitHub the only write path, Anthropic what every turn is billed against. A harness paired with a non-Anthropic connector typechecks green and fails at deploy.                                            |
| channel reach (`infra/agents/ask-cargo.ts`)               | value | **derived**: `allChannels: true`, so the reach is every channel the bot is in. Read them from the Slack connector's channel autocomplete; `cargo-ai ai agent list` shows which other agents list channels of their own.                                            | The agent reads the ICP, the pipeline and the spend out loud to whoever is in the channel. A customer shared channel the bot is in leaks all of it. A channel another agent lists stays that agent's, and a second `allChannels` agent answers alongside this one. |
| roster (`references/roster.md`)                           | value | **derived**: `cargo-ai ai agent list` for what is deployed, each agent's description for what it owns.                                                                                                                                                            | Without it the agent guesses which agent owns a job from names alone, and "re-score Acme" goes to the wrong one or gets re-done by hand.                                                                                        |

Checked before moving on, not after the deploy:

- `cargo-ai project check` prints `agent:ask_cargo bound to <your repo>#<branch>` with no trailing
  subdirectory
- every channel the bot is in is internal, or is listed on another agent that owns it, and no other
  agent's trigger is also `allChannels`
- `node --import tsx evals/contract.mjs` passes

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something.

| Variation             | When it is right                                                                                     | How                                                                                                                                                                                                  | What it costs                                                                                                                                                                                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `answer-only`         | You want a Slack oracle over the repo first, and no one running anything from Slack yet              | In `infra/agents/ask-cargo.prompt.ts`, replace §3 and §4 with "propose the command, never run it"                                                                                                    | The team copies commands out of Slack into a terminal, and "the agent said it would cost X" stops being checked against what actually ran.                                                                                            |
| `listed-channels`     | The bot sits in channels it must never answer in, or you want answers in a few channels only        | Replace `allChannels: true` with `channelIds: ["C…"]` in `infra/agents/ask-cargo.ts`, from the connector's autocomplete                                                                            | A list to keep in sync: a new team channel gets no answer until someone edits the file and deploys. Listing a channel also takes it from any `allChannels` agent.                                                                  |
| `dms-too`             | Individuals want to ask privately                                                                    | Add each person's Slack **user id** (`U…`) to `channelIds` next to `allChannels`; DMs are listed by user, not by `D…` channel, and `allChannels` never covers them.                                   | The thread stops being multiplayer: nobody else sees the proposal or the go, so a DM go is one person approving spend alone. Keep §3 unchanged if you take this.                                                                    |
| `master-agent-slack`  | You only need questions answered, no repo and no pull requests                                       | Skip this cookbook. Put a Slack trigger on the workspace's built-in Master Agent in the UI.                                                                                                          | No checkout: it cannot read `infra/` or `cadence/`, and it cannot change anything. Cheaper and faster per question, because there is no sandbox to start.                                                                           |
| `no-handoff`          | No other agents are deployed yet                                                                     | Delete §4 of the prompt and `references/roster.md`                                                                                                                                                   | Every job is redone by this agent from scratch, without the owning agent's rules. Add §4 back the day the first pipeline deploys.                                                                                                    |
| `higher-sample-bar`   | Your runs are expensive per record, or touch people                                                  | Lower the 25-record threshold and the 5-record sample in §3 of the prompt                                                                                                                            | More round trips in the thread for every batch, and each one needs another `@Cargo go`.                                                                                                                                            |
| `no-capture`          | Nobody should write the cadence log or context from Slack                                            | Delete §5 of `infra/agents/ask-cargo.prompt.ts` and its exception in the Slack-tools paragraph | Threads worth keeping are lost to Slack search. A change request still edits `context/` through §2, with no repetition bar. |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The bot is kept out of customer shared channels.** (`infra/agents/ask-cargo.ts`) The trigger is
  `allChannels`, so where the bot is invited is where the agent answers. A shared channel the bot
  joined for something else is a channel where the first question reads the ICP and the pipeline to
  the customer. Remove the bot there, or list the channel on the agent that owns it.
- **The sandbox runs as a viewer service user.** (`infra/users/index.ts`) Its `cargo-ai` session
  is what anyone in the channel can steer. With a write role, a message that talks the agent past
  its prompt can deploy or edit a resource; with no `runAs`, every workspace read fails. The
  contract fails on either.
- **Nothing on `uses`.** (`infra/agents/ask-cargo.ts`) The trigger replies by itself, so a
  `postMessage` use is a second way to post, to any channel. A sub-agent or tool on `uses` is a path
  that skips the go in the thread, and a sub-agent handle imports another cookbook's file. The
  contract fails on any of the four.
- **Spend, sends and handoffs wait for a go in the thread.** (`infra/agents/ask-cargo.prompt.ts`)
  Anyone in the channel can @mention it. Without the gate, a half-typed "enrich everything" runs a
  batch over the whole model, and the only record of who approved it is a Slack thread nobody
  reread. The go approves the proposal as written, never more records or a higher cost.
- **Changes are one pull request per thread, never a merge, never a deploy.**
  (`infra/agents/ask-cargo.prompt.ts`) The merge is the approval. An agent that deploys from Slack
  turns a mistyped message into a production change with no diff anyone read.
- **The agent never posts with the Slack tools.** (`infra/agents/ask-cargo.prompt.ts`) The trigger
  hands it `postMessage` with no channel lock, plus history. A reply is its final text, in the
  thread it was asked in; anything else is how an internal answer lands in the wrong channel. A
  capture reads only the thread it was mentioned in (`getThread`), never another channel.
- **A reply never contains a Slack user mention.** (`infra/agents/ask-cargo.prompt.ts`, How Slack
  reaches you) Slack delivers a message that names the app as a new mention, so a reply quoting
  `<@…>` wakes the agent on its own words; a live test answered one mention five times that way.
  The reply says "mention me again with go" in plain words instead.
- **A capture promotes only what repeats, and never edits the archive.**
  (`infra/agents/ask-cargo.prompt.ts` §5) A claim written to `context/` on one Slack message becomes
  what every agent believes; the bar is two independent first-hand occurrences across calls and
  threads. Raw captures are never edited, and a shared-channel thread is refused: it is the
  customer's conversation as much as ours.
- **It hands work to the owning agent instead of redoing it.** (`infra/agents/ask-cargo.prompt.ts`)
  A scorer's rules live in the scorer's prompt. Redoing the job here produces a second score with
  none of those rules, and the two disagree in the CRM.
- **It does not claim to know who asked.** (`infra/agents/ask-cargo.prompt.ts`) The model is not
  told. A pull request that names a requester names a guess.

## Done when

- `node --import tsx evals/contract.mjs` passes: harness is `claudeCode` on an Anthropic connector,
  one Slack trigger on `allChannels`, nothing on `uses`, no capability, `runAs` a viewer service user
- `cargo-ai project plan` reports the agent, the three connectors, the folder, the `ask_cargo` user and the
  adopted `viewer` role
- a question in a channel the bot is in ("what is our ICP?") got an answer in the thread that cites a file
  under `context/`
- a question about the workspace ("what failed yesterday?") cites the `cargo-ai` command it ran; a
  read that errored says so instead of a number. `cargo-ai whoami` in the sandbox names the
  `ask_cargo` service user
- a change request opened exactly one unmerged pull request, and a follow-up in the same thread
  added a commit to it rather than opening a second
- a request that spends replied with a proposal and a live price and ran nothing; the same request
  ran only after `@Cargo go`
- a request an installed agent owns was handed to it with `cargo-ai ai message create`, without
  waiting, and the reply names the new chat and where its result lands, with no promise to report back
- a mention in a channel another agent lists got that agent's reply, not this one's
- "@Cargo capture this" in an internal thread wrote `cadence/log/raw/slack/` and
  `cadence/log/slack/` files with the thread's `source:` line on the thread's pull request, reacted
  :white_check_mark:, and replied with the entry path and the pull request; a second mention with
  no new replies wrote nothing; the same request in a shared channel was refused
- every mention produced exactly one reply, and no reply contains a `<@…>` mention

## What it costs

Every turn is a harness run: a sandbox, a clone of the repository, and LLM tokens billed through the
bound Anthropic connector. A turn that only answers a question costs tokens and nothing else. The
read-only `cargo-ai` calls are API calls, not connector actions, and bill nothing.

What spends is what someone approves with a go: the connector actions, batches and agent handoffs in
§3 of the prompt. The agent reads each price live (`cargo-ai connection integration get <slug>`) and
says the total before it asks for the go, so the proposal is the cost line. Nothing runs on a
schedule.

## Composes into

Nothing in particular comes after it: it is the on-demand layer over whatever else is deployed, so
it gets more useful with every pipeline that writes logs, calls or scores it can read.

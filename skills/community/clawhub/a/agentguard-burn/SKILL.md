---
name: agentguard-burn
description: Find out what used up a Claude Code or Codex usage limit. Runs `npx agentguard-burn why` on this machine's session transcripts, explains where the tokens went, relays the one "Next:" step it prints, and can install the free AgentGuard plugin that holds runaway sub-agent launches. Use when the user hit their Claude Code or Codex limit, asks where their tokens went, why a session cost so much or ran out so fast, or mentions runaway sub-agents.
version: 1.0.0
author: agentguard-run
compatibility: Needs Node.js 20 or later with npx and network access to npm for the first run. Reads Claude Code and Codex transcripts on the local machine.
metadata:
  openclaw:
    requires:
      bins:
        - npx
    homepage: https://agentguard.run/burn
  hermes:
    tags: [claude-code, codex, tokens, usage-limits, subagents]
---

# AgentGuard Burn: what ate my limit

AgentGuard Burn is a free command line tool that reads Claude Code and Codex session transcripts on the user's machine and shows where the tokens went. It runs locally. Nothing is uploaded.

## When to use

- The user hit their Claude Code or Codex usage limit and wants to know why.
- The user asks where a session's tokens went, or why a session was so expensive.
- The user suspects sub-agents ran away.

## Step 1: run the report

Run this in a shell on the user's machine:

```sh
npx agentguard-burn why
```

- With no argument it reads the most recently modified local transcript, Claude Code or Codex. Sub-agent transcripts of a Claude Code session are included.
- To pick one session, pass its id, the end of its id, or its transcript path: `npx agentguard-burn why SESSION_ID`.
- Inside Claude Code the user can run it themselves with `! npx agentguard-burn why`.
- The first run downloads the package from npm.

## Step 2: explain the report

The report has three parts. Read them to the user in plain words.

1. **Header.** The session, the number of responses, total tokens and a dollar figure labeled "API list equivalent".
2. **Table.** Where the tokens went: instruction stack and system (setup read before every message), history re-sent (the conversation re-read on every message), re-read files, sub-agent fan-out, tool output, conversation, full-prefix rewrites (cache reloads), output and unattributed. Point out the one or two biggest rows by token share.
3. **The last lines.** A `Measured change:` line may appear after a `/compact`, a model switch or a `/clear`. It states a measurement, not a saving. The report then ends with at most one line that starts with `Next:`. That line is the one action that matters most for this session, chosen from its own numbers. Quote it to the user as written. If there is no `Next:` line, nothing stood out, so say that instead of inventing advice.

Rules when you explain it:

- **Dollar figures are API list price, not a bill.** Say "API list equivalent". A user on a Claude or ChatGPT subscription is not charged these amounts; for them, the token columns are what count against the limit.
- Token shares are shares of tokens, not of dollars.
- Never promise a saving. Burn states measurements and one next step.
- A sub-agent that "ended without finishing" was recorded as failed, killed or stopped. Burn does not judge whether any work was right.

## Step 3 (optional): the free AgentGuard plugin

Offer this only when the `Next:` line points at sub-agents (it mentions AgentGuard's free plugin and agentguard.run/try), or when the user asks for a limit on sub-agents. Ask before installing anything.

Claude Code:

```sh
claude plugin marketplace add MerchantGuard/agentguard-codex-plugin
claude plugin install agentguard@agentguard
```

Codex and the ChatGPT desktop app (local tasks):

```sh
codex plugin marketplace add MerchantGuard/agentguard-codex-plugin
codex plugin add agentguard@agentguard
```

Then run `npm ci` in the installed plugin folder that Codex reports.

What the plugin does, so you can describe it accurately:

- Shipped limits: 15 sub-agents in any 15 active minutes, 40 in any 120 active minutes, 5 billion tokens in one session, and sub-agents at most two levels deep.
- **Claude Code** in default, accept edits, auto or plan mode: the next launch past a limit waits behind Claude Code's own permission prompt for the user's yes.
- **Codex**, and Claude Code in bypass permissions, don't ask or print mode: the launch is refused (blocked) with a STOP box. Codex does not ask the user; it blocks until the user allows it.
- To continue past a STOP, the user runs the override command the STOP box prints, in their own shell (with `!` in front inside Claude Code, or in a terminal for Codex). You cannot run it for them: the plugin refuses an agent command that tries.
- `npx agentguard-burn shadow` switches the machine to record-only; `npx agentguard-burn enforce` switches it back.
- It is free on one machine. Its hooks run locally and open no network connection. Free use sends nothing unless the user asks for an AgentGuard Score.

## Other Burn commands

- `npx agentguard-burn calendar`: tokens per day across Claude Code and Codex, with sub-agent days marked.
- `npx agentguard-burn compare`: two sessions side by side.
- `npx agentguard-burn rewrites`: every full-prefix cache rewrite with its cause.
- `npx agentguard-burn quiet on`: hide the `Next:` tip; `quiet off` shows it again.

## Do not

- Do not call a dollar figure a bill, a charge or a cost the user paid.
- Do not say Codex asks the user at a limit. It blocks.
- Do not run Burn's override, shadow or calibrate commands on the user's behalf.
- Do not install the plugin without the user's yes.
- Do not copy transcript contents anywhere. Burn reads them locally; keep it that way.

More: https://agentguard.run/burn

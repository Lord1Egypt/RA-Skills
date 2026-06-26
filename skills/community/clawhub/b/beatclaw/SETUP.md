# BeatClaw — Skill Setup

## Install (one line)

### Option A — From beatclaw.com (recommended)

```bash
mkdir -p ~/.claude/skills/beatclaw && \
  curl -fsSL https://beatclaw.com/skill -o ~/.claude/skills/beatclaw/SKILL.md
```

For OpenClaw: replace `~/.claude/skills/` with `~/.openclaw/skills/`.

### Option B — Via ClawHub

```bash
npm i -g clawhub      # one-time
clawhub install beatclaw
```

### Option C — Tell your agent

In a Claude Code (or OpenClaw) session, just paste:

> Install the BeatClaw skill from https://beatclaw.com/skill

Your agent will fetch and save it for you.

---

### Start a new session

The skill loads on session start. Your agent will see **beatclaw** in its available skills and will walk you through first-time setup:

1. **Owner email** — verified via 6-digit code
2. **PayPal email** — for receiving payouts (80% of each sale)
3. **Suno API key** — from [apiframe.ai](https://app.apiframe.ai) or [sunoapi.org](https://sunoapi.org) (you pay the provider directly)
4. **Pricing** — WAV track price ($2.99+) and WAV+Stems price ($9.99+)

The agent handles registration, API key storage, and configuration automatically.

## Requirements

- A third-party Suno API key (apiframe.ai or sunoapi.org)
- `curl` on PATH (used for all API calls)
- PayPal account for receiving payouts

## Verify it's working

Ask your agent:

> "What skills do you have?"

It should list **beatclaw**. Then:

> "Make me a beat"

The agent will generate, poll, and publish — all automatic.

## Stem Splitting (recommended)

**MVSEP is the default** for stem splitting — it's free and uses the high-quality BS Roformer SW model.

1. Get a free API key at [mvsep.com/user-api](https://mvsep.com/user-api)
2. Tell your agent to store it (or set it manually via `update-agent-settings`)

Without an MVSEP key, agents using sunoapi.org can fall back to built-in splitting (50 credits per split, 12 stems). Agents using apiframe.ai with no MVSEP key cannot split stems.

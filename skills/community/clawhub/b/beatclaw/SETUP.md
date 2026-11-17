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

### Before the agent can do anything: create your producer

An agent cannot create a producer — you do, at **[beatclaw.com](https://beatclaw.com)** (menu → sign up as a producer). It belongs to the email you sign in with. Then, in your dashboard:

- **Security → Log in with PayPal.** That account becomes your payout address. The producer cannot generate until this is done.
- **Your producer → Settings → paste your Suno API key**, from [sunoapi.org](https://sunoapi.org) (pay-as-you-go).

### Start a new session, and let the agent in

The skill loads on session start. Tell your agent which producer to work as:

> "Connect to @yourproducer on BeatClaw"

It shows you a short code and a link. Open the link — or type the code into **Connect an agent** in your dashboard — and approve. The agent collects its own token; you never see one and never paste one.

**Your agent never asks you for an email code, an authenticator code, an API key or a PayPal address, and you should not send it one.** It has nowhere to put them — the platform refuses all of them from an agent.

The same agent can work as several producers, including producers that belong to different people. Each one is a separate request that its own owner approves.

## Requirements

- `curl` on PATH (used for all API calls)
- A PayPal account, to be paid (80% of each sale, 14 days after it)

## Verify it's working

Ask your agent:

> "What skills do you have?"

It should list **beatclaw**. Then:

> "Make me a beat"

The agent will generate, poll, and publish — all automatic.

## Stem Splitting (recommended)

Stems are split on **MVSEP** — free, using the BS Roformer SW model.

1. Get a free API key at [mvsep.com/user-api](https://mvsep.com/user-api)
2. Paste it into **your producer → Settings** at beatclaw.com

Like the Suno key, it goes into the dashboard, not to your agent.

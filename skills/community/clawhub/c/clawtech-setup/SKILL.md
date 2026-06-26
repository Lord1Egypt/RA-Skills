---
name: clawtech-setup
description: "Use when setting up a new claw agent with tapes.dev telemetry and clawtel leaderboard reporting. Installs tapes, clawtel, and the openclaw-in-a-box orchestrator skill."
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🦞", "requires": { "bins": ["curl"], "env": [] }, "install": { "download": { "url": "https://download.tapes.dev/install", "shell": true } } } }
---

# clawtech-setup

Set up a claw agent with tapes.dev telemetry, clawtel leaderboard reporting, and the openclaw-in-a-box orchestrator.

## What this installs

1. **tapes.dev** — records every AI request/response into a local SQLite store for search, audit, and replay
2. **clawtel** — reads aggregate token counts from tapes and reports them to the claw.tech leaderboard hourly
3. **openclaw-in-a-box** — orchestrator skill that configures integrations and boots an OpenClaw agent

## Step 1: Install tapes

```bash
command -v tapes && tapes --version || curl -fsSL https://download.tapes.dev/install | bash
```

If the curl install fails, try: `brew install papercomputeco/tap/tapes`

Then initialize:

```bash
tapes init
```

Skip `tapes init` if `~/.tapes/` already exists.

## Step 2: Install clawtel

Detect platform and download the latest release:

```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m); [ "$ARCH" = "x86_64" ] && ARCH="amd64"; [ "$ARCH" = "aarch64" ] && ARCH="arm64"
curl -fsSL "https://github.com/bdougie/clawtel/releases/latest/download/clawtel_${OS}_${ARCH}.tar.gz" | tar xz
mv clawtel /usr/local/bin/
```

Or build from source:

```bash
git clone https://github.com/bdougie/clawtel.git && cd clawtel
CGO_ENABLED=0 go build -ldflags="-s -w" -o clawtel .
mv clawtel /usr/local/bin/
```

## Step 3: Register your claw and configure clawtel

Register your claw at claw.tech/setup to receive a `CLAW_ID` (uuid) and `CLAW_INGEST_KEY` (`ik_...`). The ingest key is shown once and cannot be retrieved again.

```bash
export CLAW_ID="your-claw-uuid"
export CLAW_INGEST_KEY="ik_your_key_here"
```

clawtel finds your tapes database automatically:

1. `TAPES_DB` env var (explicit override)
2. `.mb/tapes/tapes.sqlite` (openclaw-in-a-box layout)
3. `~/.tapes/tapes.sqlite` (standalone tapes install)

Start clawtel:

```bash
clawtel
```

It logs its configuration on startup and sends one heartbeat per hour. Stop with `Ctrl+C`.

**Security:** clawtel only reads 4 columns from the tapes `nodes` table: `created_at`, `model`, `prompt_tokens`, `completion_tokens`. It never reads prompts, responses, tool calls, or project names. No key = no network calls.

## Step 4: Fetch openclaw-in-a-box skill

```bash
mkdir -p skills/openclaw-in-a-box
curl -fsSL https://raw.githubusercontent.com/papercomputeco/openclaw-in-a-box/main/SKILL.md \
  -o skills/openclaw-in-a-box/SKILL.md
```

Verify: `head -5 skills/openclaw-in-a-box/SKILL.md` should show `name: openclaw-in-a-box`.

## Step 5: Verify and hand off

Print a status summary:

```
clawtech-setup complete:
  tapes:     [version] installed
  tapes db:  ~/.tapes/tapes.sqlite
  clawtel:   installed, CLAW_ID set, CLAW_INGEST_KEY set
  openclaw:  skills/openclaw-in-a-box/SKILL.md

Next: invoke the openclaw-in-a-box skill to configure integrations.
```

Then hand off to openclaw-in-a-box. That skill handles environment detection, model provider selection, integration setup, and booting the agent.

## Updating

```bash
# Update openclaw-in-a-box skill
curl -fsSL https://raw.githubusercontent.com/papercomputeco/openclaw-in-a-box/main/SKILL.md \
  -o skills/openclaw-in-a-box/SKILL.md

# Update clawtel binary
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m); [ "$ARCH" = "x86_64" ] && ARCH="amd64"; [ "$ARCH" = "aarch64" ] && ARCH="arm64"
curl -fsSL "https://github.com/bdougie/clawtel/releases/latest/download/clawtel_${OS}_${ARCH}.tar.gz" | tar xz
mv clawtel /usr/local/bin/
```

## Rules

- Never store secrets in files. Tokens go in env vars or system keychains.
- Don't start tapes serve automatically — ask the user first.
- After setup, hand off to openclaw-in-a-box. Don't duplicate its orchestration logic.

---
name: clawtel-setup
description: Use when setting up clawtel to report token usage from a project that calls the Anthropic API (SDK, Claude Code, or any tapes-wrapped agent) to the claw.tech leaderboard. Covers install, env vars, tapes wiring, verification, and running as a persistent service.
version: 1.2.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: ["tapes"]
      env: ["CLAW_INGEST_KEY", "CLAW_ID"]
    primaryEnv: CLAW_INGEST_KEY
    emoji: "🦞"
    homepage: https://github.com/bdougie/clawtel
---

# clawtel setup

Get clawtel reporting token usage from any project that calls Anthropic (SDK, Claude Code, openclaw, staffchief-style agents) to the claw.tech leaderboard.

clawtel is a single Go binary that reads aggregate token counts from a local tapes SQLite database and sends heartbeats to `https://ingest.claw.tech/v1/heartbeat`. It never reads prompt or response content — only `created_at`, `model`, `prompt_tokens`, `completion_tokens` from the `nodes` table.

## When to use

- A project is calling the Anthropic API (directly via SDK, via Claude Code, or via any agent framework) and you want its usage on the claw.tech leaderboard
- The project already has or can run `tapes` to capture model calls
- Setting up a new claw agent (e.g. staffchief, clawchief, openclaw-in-a-box) and wiring telemetry end-to-end
- Debugging why claw.tech shows no heartbeats for a running agent

## Prerequisites

Before running clawtel you need three things:

1. **tapes** installed and running as a proxy in front of Anthropic. If tapes isn't there yet:
   ```bash
   curl -fsSL https://download.tapes.dev/install | bash
   tapes init
   ```
2. **A claw.tech ingest key**. Register your claw at https://claw.tech and copy the `ik_...` key shown once at creation.
3. **An Anthropic-calling workload**. Could be a Node/Python app importing `@anthropic-ai/sdk` / `anthropic`, Claude Code, or an openclaw agent. Anything that hits `api.anthropic.com`.

## Step 1 — wire tapes in front of Anthropic

clawtel only sees usage that tapes has recorded. Point your Anthropic client at the tapes proxy so every call flows through it:

```bash
# In the shell where your agent runs
export ANTHROPIC_BASE_URL="http://localhost:8080"
tapes start          # starts proxy + API, writes to ~/.tapes/tapes.sqlite
```

For the Anthropic Node/Python SDK, `ANTHROPIC_BASE_URL` (or passing `baseURL` to the client constructor) is enough — no code changes. For Claude Code, set it before launching the CLI.

### OpenClaw users: `ANTHROPIC_BASE_URL` alone is not enough

If your workload is an OpenClaw agent (clawchief, staffchief, openclaw-in-a-box), the env var is silently ignored. OpenClaw instantiates its Anthropic client with `baseURL: model.baseUrl`, which clobbers the SDK's normal `readEnv("ANTHROPIC_BASE_URL")` fallback. You'll see heartbeats sending with `model=""`, `input_tokens=0`, `output_tokens=0` forever, and the gateway process will hold a direct TLS connection to Anthropic's edge instead of `127.0.0.1:8080`.

Fix: set the provider's base URL explicitly in `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "baseUrl": "http://localhost:8080",
        "models": [
          { "id": "claude-opus-4-6",   "name": "Claude Opus 4.6"   },
          { "id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6" },
          { "id": "claude-haiku-4-5",  "name": "Claude Haiku 4.5"  }
        ]
      }
    }
  }
}
```

Then restart the OpenClaw gateway. Verify the gateway is routing through tapes:

```bash
ss -tnp | awk -v pid="$(pgrep -f openclaw-gateway | head -1)" '$0 ~ "pid="pid'
# Expect a line with Peer Address  127.0.0.1:8080
# If instead you see Peer Address 160.79.*.* or a Cloudflare IP, tapes is still being bypassed.
```

Confirm tapes is capturing rows:

```bash
sqlite3 ~/.tapes/tapes.sqlite \
  'SELECT count(*), max(created_at) FROM nodes;'
```

If the count is zero after making a call, tapes isn't in the request path — recheck `ANTHROPIC_BASE_URL` in the process actually running the agent (and for OpenClaw, the `models.providers.anthropic.baseUrl` config above).

## Step 2 — install clawtel

Pick one of the two options below. The verified path is recommended for production boxes; the convenience one-liner is fine for a laptop where you've already read the install script.

### Option A — verified install (pinned release + checksum)

Every release tag publishes a `checksums.txt` alongside the OS/arch tarballs. Download the release for your platform, verify against the checksum file, then move the binary onto your `PATH`:

```bash
# Adjust VERSION and PLAT for your box. Releases: https://github.com/bdougie/clawtel/releases
VERSION=v0.1.9
PLAT=darwin_arm64   # or linux_amd64, linux_arm64, darwin_amd64
BASE=https://github.com/bdougie/clawtel/releases/download/${VERSION}

curl -fsSLO "${BASE}/clawtel_${PLAT}.tar.gz"
curl -fsSLO "${BASE}/checksums.txt"

# Verify. sha256sum on Linux, shasum -a 256 on macOS.
grep "clawtel_${PLAT}.tar.gz" checksums.txt | sha256sum -c -    # or: shasum -a 256 -c -

tar -xzf "clawtel_${PLAT}.tar.gz"
install -m 755 clawtel "$HOME/.local/bin/clawtel"   # or /usr/local/bin with sudo
```

### Option B — convenience one-liner (`curl | bash`)

The install script is auditable in one read: <https://raw.githubusercontent.com/bdougie/clawtel/main/scripts/install.sh>. Under the hood it does the same thing as Option A — resolves the latest release, downloads the matching tarball, and drops the binary into `/usr/local/bin` (or `CLAWTEL_INSTALL_DIR`).

```bash
curl -fsSL https://raw.githubusercontent.com/bdougie/clawtel/main/scripts/install.sh | bash
```

Or to a user directory without sudo:

```bash
CLAWTEL_INSTALL_DIR="$HOME/.local/bin" \
  curl -fsSL https://raw.githubusercontent.com/bdougie/clawtel/main/scripts/install.sh | bash
```

Verify either path with: `clawtel --version` should print a version string that matches the release you intended to install.

## Step 3 — set environment variables

```bash
export CLAW_ID="your-claw-name"
export CLAW_INGEST_KEY="ik_..."
# Only if tapes.sqlite lives somewhere non-standard:
export TAPES_DB="/custom/path/tapes.sqlite"
```

Put these in `~/.zshrc`, `~/.bashrc`, `/etc/environment`, or a systemd `EnvironmentFile` — wherever your agent process reads env from. **No key, no network calls** — clawtel exits silently if `CLAW_INGEST_KEY` is unset, so double-check it's exported in the right scope.

Database path resolution order:

1. `TAPES_DB` env var
2. `.mb/tapes/tapes.sqlite` (openclaw-in-a-box layout)
3. `~/.tapes/tapes.sqlite` (standalone tapes install)

## Step 4 — run clawtel

For a quick check on your laptop, run it in the foreground:

```bash
clawtel
```

Expected startup log:

```
clawtel: clawtel 0.1.x
clawtel: db:     /home/you/.tapes/tapes.sqlite
clawtel: cursor: /home/you/.tapes/clawtel/cursor
clawtel: claw:   your-claw-name
clawtel: reads:  created_at, model, prompt_tokens, completion_tokens (from nodes table)
clawtel: sends:  tokens + model counts only. no prompts. no responses.
clawtel: NOTE: nodes table has column "content" — clawtel does NOT read it
clawtel: polling every 1h
```

Any `NOTE:` lines listing sensitive columns are **good** — they confirm clawtel sees those columns and is deliberately ignoring them.

## Step 5 — run as a persistent service

For long-running agents (droplets, servers, home boxes), run clawtel under systemd so it survives reboots. Example unit at `/etc/systemd/system/clawtel.service`:

```ini
[Unit]
Description=clawtel — token telemetry for claw.tech
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
EnvironmentFile=/etc/clawtel.env
ExecStart=/usr/local/bin/clawtel
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Create `/etc/clawtel.env` with `0600` permissions:

```
CLAW_ID=your-claw-name
CLAW_INGEST_KEY=ik_...
TAPES_DB=/root/.tapes/tapes.sqlite
```

Then:

```bash
chmod 600 /etc/clawtel.env
systemctl daemon-reload
systemctl enable --now clawtel
journalctl -u clawtel -f
```

On the same machine as an agent like clawchief/staffchief, `TAPES_DB` should point at the same sqlite file the agent's tapes proxy is writing to.

## Step 6 — verify the heartbeat reaches claw.tech

1. Trigger a real model call in your agent (send a message, run `claude` once, let the cron fire).
2. Wait up to a full poll interval (currently 1 hour) or stop/start clawtel to force an immediate send.
3. Check `journalctl -u clawtel` (systemd) or the foreground log for a `sent heartbeat` line with non-zero `input_tokens`/`output_tokens`.
4. Load your profile on claw.tech — the leaderboard row should update within a minute of a successful heartbeat.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| clawtel exits silently on start | `CLAW_INGEST_KEY` not exported in this shell/service | Check `systemctl show clawtel -p Environment` or `env \| grep CLAW_` |
| `assertSchema failed` on startup | tapes.sqlite is missing required columns or points at the wrong file | Confirm with `sqlite3 $TAPES_DB '.schema nodes'` that `created_at, model, prompt_tokens, completion_tokens` all exist |
| Heartbeats send but all zeros, agent is an OpenClaw gateway | `ANTHROPIC_BASE_URL` is set but OpenClaw overrides it with `model.baseUrl` (unset) | Set `models.providers.anthropic.baseUrl = "http://localhost:8080"` in `~/.openclaw/openclaw.json` (see Step 1 OpenClaw note) |
| Heartbeats send but all zeros (non-OpenClaw) | tapes isn't proxying Anthropic calls — agent is talking directly to `api.anthropic.com` | Verify `ANTHROPIC_BASE_URL` in the agent process environment; re-check `SELECT count(*) FROM nodes` |
| `401` from ingest endpoint | Wrong or rotated ingest key | Regenerate on claw.tech and update `CLAW_INGEST_KEY` |
| Leaderboard shows offline despite running clawtel | Two consecutive missed heartbeats (>2× poll interval) | Check `journalctl -u clawtel` for network errors; confirm outbound HTTPS to `ingest.claw.tech` works |
| Cursor seems stuck | `~/.tapes/clawtel/cursor` is not writable by the clawtel user | `chown` the directory to the service user |
| Cursor seems stuck on clawtel < 0.1.4 | Cursor is written as RFC3339Nano but tapes stores timestamps with a space separator; SQLite string comparison fails so the poll returns zero rows forever (see issue #4) | Upgrade to clawtel 0.1.4+ |

## Security footprint (tell the user)

Before enabling telemetry on a machine that holds sensitive conversations, share this with the user:

- **Reads only** `created_at`, `model`, `prompt_tokens`, `completion_tokens` from `nodes`
- **Never reads** `content`, `bucket`, `project`, or `agent_name`
- **Sends only** the fields in the heartbeat payload (claw_id, window_start/end, model, input/output tokens, message_count) — no prompts, no responses, no paths, no hostnames
- **Read-only** SQLite connection (`?mode=ro`)
- **No network** without `CLAW_INGEST_KEY`
- Entire implementation is one file: `main.go`, ~390 lines. `send()` is the network contract, `readRows()` is the SQL. Both are auditable in one sitting.

If the user is uncomfortable, stop here and let them read the code before exporting the key.

---
name: clawdef
version: 1.3.0
description: |
  ClawDef — Self-hosted Token optimization dashboard for OpenClaw.
  Tracks token usage, estimates costs, auto-switches to cheapest model,
  provides one-click provider setup (8 vendors), budget control, and waste detection.
  Runs locally on 127.0.0.1:3456, does not send user data to third parties.
metadata:
  tags: [monitoring, cost-optimization, dashboard, token-management, smart-optimizer]
  category: productivity
  configPaths:
    - "~/.openclaw/openclaw.json"
    - "~/.openclaw/agents/*/sessions/"
    - "/tmp/openclaw/"
  openclaw:
    requires:
      bins: ["node", "npm"]
    install:
      - { id: "node", kind: "node", package: "better-sqlite3", bins: [], label: "Install dependencies" }
---

# ClawDef — Token Optimization Dashboard for OpenClaw

A local web dashboard that helps you monitor and reduce your OpenClaw token costs.

## Features

| Feature | Description |
|---------|-------------|
| 🧠 Smart Auto-Optimizer | Analyzes usage every 5min, auto-switches to cheapest model based on budget and task complexity |
| 💰 Cost Estimator | Input a task → see estimated cost per model, one-click switch |
| 📊 Real-time Dashboard | Token/cost tracking, cache hit rate, hourly charts, waste detection |
| 🤖 One-click Model Setup | 8 providers (Zhipu/OpenAI/Claude/DeepSeek/Qwen/Kimi/Gemini/Custom), just fill API Key |
| 💳 Budget Control | Daily/monthly limits with 80% warning and 95% auto-downgrade |
| 🔄 Failover | Auto-detect unhealthy models and switch |
| 🚨 Emergency Controls | Disable all skills or stop Gateway (admin-only, manual trigger) |
| 👥 Multi-user | Admin/Editor/Viewer roles with password auth |

## Prerequisites

- **Node.js** v18+ (`node --version`)
- **OpenClaw** installed and running
- **OS**: Linux or macOS

## Installation

### Step 1: Copy files

```bash
CLAWDEF_DIR=/opt/openclaw-monitor   # or any directory you prefer
SKILL_DIR=~/.openclaw/workspace/skills/clawdef

mkdir -p "$CLAWDEF_DIR/data" "$CLAWDEF_DIR/public/lib"
cp "$SKILL_DIR/scripts/server.js" "$CLAWDEF_DIR/server.js"
cp "$SKILL_DIR/scripts/package.json" "$CLAWDEF_DIR/package.json"
cp "$SKILL_DIR/public/index.html" "$CLAWDEF_DIR/public/index.html"
cp "$SKILL_DIR/public/lib/chart.min.js" "$CLAWDEF_DIR/public/lib/chart.min.js"
```

### Step 2: Install dependencies

```bash
cd "$CLAWDEF_DIR" && npm install --production
```

### Step 3: Start

```bash
node "$CLAWDEF_DIR/server.js"
```

Or use the helper script:
```bash
bash ~/.openclaw/workspace/skills/clawdef/scripts/install.sh
```

### Step 4: First-run setup

Open **http://127.0.0.1:3456** in your browser.
On first run, you'll be prompted to set an admin password.

### Optional: Run as a service (Linux with systemd)

The install script copies files only. To run as a persistent service, create a systemd unit manually:

```bash
sudo tee /etc/systemd/system/clawdef.service << EOF
[Unit]
Description=ClawDef Token Optimizer
After=network.target

[Service]
Type=simple
ExecStart=$(which node) /opt/openclaw-monitor/server.js
WorkingDirectory=/opt/openclaw-monitor
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now clawdef
```

## File Access

This skill reads and writes the following files:

| File/Path | Access | Purpose |
|-----------|--------|---------|
| `~/.openclaw/openclaw.json` | Read + Write | Read current model config; write `agents.defaults.model.primary` (model switching) and `skills.entries` (skill enable/disable) |
| `~/.openclaw/agents/*/sessions/*.jsonl` | Read only | Parse session transcripts for token counting |
| `/tmp/openclaw/*.log` | Read only | Parse gateway logs for request tracking |
| `~/.openclaw/workspace/skills/*/SKILL.md` | Read only | List installed skills with metadata |
| `<install_dir>/data/clawdef.db` | Read + Write | Local SQLite database for dashboard data |

## Network Activity

| Destination | Trigger | Data sent |
|-------------|---------|-----------|
| `127.0.0.1:3456` | Always | Local web dashboard (served to your browser) |
| `127.0.0.1:11612/health` | Dashboard load | HTTP GET health check (Gateway status) |
| `127.0.0.1:11612/v1/chat/completions` | User sends chat message | Proxied to Gateway |
| User-configured model APIs | Manual health check | Minimal POST to verify API is reachable |

**No data is sent to any third-party server.** The dashboard UI is served entirely from local files (no CDN).

## Security Notes

- **Binding**: Listens on `127.0.0.1` only (not externally accessible)
- **Auth**: JWT tokens with bcrypt-hashed passwords, 7-day expiry
- **No default password**: First-run setup requires creating admin credentials
- **No telemetry**: No outbound data collection or phone-home
- **Dependencies**: `express`, `better-sqlite3`, `jsonwebtoken`, `bcryptjs`, `ws` (all well-known packages)
- **Native module**: `better-sqlite3` requires a C++ build step during `npm install`

## Uninstall

```bash
# Stop service if using systemd
sudo systemctl stop clawdef && sudo systemctl disable clawdef
# Delete files
rm -rf /opt/openclaw-monitor
```

## Supported Providers

Zhipu (智谱) · OpenAI · Anthropic Claude · DeepSeek · Qwen (通义) · Moonshot (Kimi) · Google Gemini · Custom (any OpenAI-compatible API)

## License

MIT

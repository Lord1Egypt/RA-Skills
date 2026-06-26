# Feishu Relay

**Safe Mode: Minimal by default, production capabilities opt-in**

A Feishu (Lark) notification bridge for OpenClaw.

---

## Two Modes

### Default Mode (ClawHub Install)

Safe, minimal, no system modifications.

```bash
openclaw skill install feishu-relay
```

**What you get:**
- ✅ Send messages via `./run.sh`
- ✅ JSON structured output
- ✅ Retry on failure
- ✅ No system modifications
- ✅ No root required

**Best for:** Personal computers, shared hosting, testing, ClawHub distribution.

---

### Production Mode (Self-Hosted Server)

For your own Linux server with 24/7 uptime requirements.

```bash
# After base install, enable production capabilities:
./scripts/install-systemd.sh --install --user      # 24/7 daemon
./scripts/install-watchdog.sh --install           # Health monitoring
sudo ./scripts/install-global-notify.sh --install  # /usr/local/bin/notify
```

**What you get (in addition to defaults):**
- 🔧 Systemd service with auto-restart
- 🔧 Watchdog health monitoring
- 🔧 Global `/usr/local/bin/notify` command

**Best for:** Your own server, 24/7 operations, production workloads.

See [docs/production.md](docs/production.md) for full production deployment guide.

---

## Quick Start

### 1. Install

```bash
openclaw skill install feishu-relay
```

### 2. Configure

```bash
export FEISHU_APP_ID="cli_xxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxx"
export FEISHU_RECEIVE_ID="ou_xxxxxxxx"
```

Or create `config.json`:

```json
{
  "appId": "cli_xxxxxxxx",
  "appSecret": "xxxxxxxx",
  "receiveId": "ou_xxxxxxxx"
}
```

### 3. Test

```bash
./run.sh -t "Test" -m "Hello from feishu-relay"
```

---

## Usage

```bash
# Basic message
./run.sh -t "Title" -m "Message"

# JSON output (for scripting)
./run.sh -t "Title" -m "Message" --json

# With receive ID override
./run.sh -t "Title" -m "Message" --receive-id ou_xxxx --receive-id-type open_id
```

---

## Configuration

| Option | Env Variable | Required | Default |
|--------|-------------|----------|---------|
| App ID | `FEISHU_APP_ID` | Yes | - |
| App Secret | `FEISHU_APP_SECRET` | Yes | - |
| Receive ID | `FEISHU_RECEIVE_ID` | Yes | - |
| ID Type | `FEISHU_RECEIVE_ID_TYPE` | No | `open_id` |

ID types: `open_id`, `user_id`, `chat_id`, `email`

---

## Project Structure

```
feishu-relay/
├── run.sh                 # Main entry point
├── notify                 # CLI wrapper
├── lib/send.py            # Core sending logic
├── config.json.example    # Config example
├── scripts/
│   ├── install-systemd.sh       # Production: systemd service
│   ├── install-watchdog.sh      # Production: health monitoring
│   ├── install-global-notify.sh # Production: global command
│   ├── install-crontab.sh       # Production: cron jobs
│   └── install-discovery.sh     # Scan for other skills
├── docs/
│   ├── advanced.md        # Opt-in capabilities
│   ├── production.md       # Production deployment guide
│   ├── security.md         # Security considerations
│   └── uninstall.md        # Removal guide
└── SKILL.md               # OpenClaw skill metadata
```

---

## Safety

- **No system modifications by default**
- **No root required for basic use**
- **No auto-migration**
- **Production capabilities are opt-in only**

---

## Documentation

| Doc | What |
|-----|------|
| [SKILL.md](SKILL.md) | Quick reference |
| [README.md](README.md) | This file |
| [docs/advanced.md](docs/advanced.md) | Opt-in capabilities |
| [docs/production.md](docs/production.md) | Production deployment |
| [docs/security.md](docs/security.md) | Security guide |
| [docs/uninstall.md](docs/uninstall.md) | Complete removal |

---

## License

MIT-0

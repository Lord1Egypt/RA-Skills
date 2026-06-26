# Chromium Skill for OpenClaw

Headless Chromium with a persistent profile and CDP (Chrome DevTools Protocol) remote debugging. Browse websites, click buttons, fill forms, take screenshots, and import cookies — all from your OpenClaw agent.

## Prerequisites

- **OpenClaw** installed and running with gateway + browser tool support
- **Chromium** (or Google Chrome) installed on the host

### Installing Chromium

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install -y chromium-browser
```

**Ubuntu (snap, often pre-installed):**
```bash
sudo snap install chromium
```

**Alpine:**
```bash
apk add chromium
```

**macOS:**
```bash
brew install --cask chromium
```

If your binary has a non-standard name or path, set `CHROMIUM_BIN`:
```bash
export CHROMIUM_BIN=/usr/bin/google-chrome
```

## Installation

```bash
clawhub install chromium
```

Or manually: copy the `chromium` folder into your OpenClaw workspace `skills/` directory and restart the session.

## Setup (one-time)

### 1. Launch Chromium

```bash
~/.openclaw/workspace/skills/chromium/scripts/start_chromium.sh
```

### 2. Verify it's running

```bash
curl -s http://127.0.0.1:18801/json/version
```

You should see JSON with `Browser` and `webSocketDebuggerUrl`. If not — check the log:
```bash
cat ~/.openclaw/workspace/logs/chromium.log
```

### 3. Done

Start a new OpenClaw session. The agent will now use headless Chromium for any browser tasks.

## Usage examples

Ask your agent:

- "Open https://example.com and tell me what's on the page"
- "Go to Hacker News and list the top 5 stories"
- "Take a screenshot of https://github.com"
- "Fill in the search box on Google and search for OpenClaw"

## Configuration

All settings are optional environment variables. Set them before running `start_chromium.sh`:

| Variable | Default | Description |
|---|---|---|
| `CHROMIUM_PROFILE_DIR` | `~/.openclaw/workspace/chromium-profile` | Persistent browser profile directory |
| `CHROMIUM_DEBUG_PORT` | `18801` | CDP port (change if 18801 is taken) |
| `CHROMIUM_LOG_FILE` | `~/.openclaw/workspace/logs/chromium.log` | Log file location |
| `CHROMIUM_BIN` | auto-detect | Path to Chromium/Chrome binary |

Example with custom port:
```bash
CHROMIUM_DEBUG_PORT=9222 ~/.openclaw/workspace/skills/chromium/scripts/start_chromium.sh
```

## Cookie import (optional)

To access sites that require login without typing credentials in headless mode:

1. In your regular browser, install the [Cookie-Editor](https://cookie-editor.com/) extension
2. Go to the target site and make sure you're logged in
3. Export cookies as JSON → save as `cookies.json`
4. Copy to your server: `scp cookies.json yourserver:/tmp/`
5. Import:
   ```bash
   python3 ~/.openclaw/workspace/skills/chromium/scripts/import_cookies.py \
     /tmp/cookies.json --domain example.com
   ```
6. Ask your agent to navigate to the site — it should be logged in

## Auto-start on boot (optional)

To launch Chromium automatically when the system starts, add a cron entry:

```bash
crontab -e
```

Add:
```
@reboot ~/.openclaw/workspace/skills/chromium/scripts/start_chromium.sh
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `Address already in use` | Another Chromium is running. Run `pkill -f "chromium.*remote-debugging"` and try again |
| CDP doesn't respond | Check the log file for errors. Common cause: missing dependencies (`libnss3`, `libatk-bridge2.0-0`) |
| `No Chromium/Chrome binary found` | Install Chromium or set `CHROMIUM_BIN` to the correct path |
| Stale `SingletonLock` | The script handles this automatically. If it persists: `rm ~/.openclaw/workspace/chromium-profile/SingletonLock` |
| Cookie import fails | Make sure the OpenClaw gateway is running (`openclaw gateway run`) |

### Missing system libraries (headless Linux)

If Chromium crashes on a minimal server, you may need:
```bash
sudo apt install -y libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libgbm1 libasound2
```

## Files

```
chromium/
├── SKILL.md                      # Skill instructions for the agent
├── README.md                     # This file
└── scripts/
    ├── start_chromium.sh          # Launch script
    └── import_cookies.py          # Cookie import utility
```

## License

Public domain. Use however you like.

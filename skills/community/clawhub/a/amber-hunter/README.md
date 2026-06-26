# 🌙 Amber-Hunter

> A local perception engine for [Huper琥珀](https://huper.org) — turns your AI collaboration sessions into frozen, searchable personal memories.

**Amber-Hunter** runs on Mac, Windows, and Linux, constantly watching your OpenClaw agent sessions. When you're ready to freeze "this moment", it captures the conversation context, recent file changes, and stores everything in an encrypted local capsule — ready to be searched and woken anytime.

---

## What It Does

- **Session Capture** — Reads OpenClaw session transcripts, extracts meaningful user/assistant exchanges
- **File Monitoring** — Tracks recently modified workspace files automatically
- **Instant Freeze** — One click to capture "what am I working on right now"
- **Local Encryption** — AES-256-GCM, master password never leaves your Mac
- **Cloud Sync (optional)** — Encrypts before uploading to your [huper.org](https://huper.org) account

---

## Installation

### Prerequisites
- macOS / Windows / Linux
- Python 3.10+
- [OpenClaw](https://github.com/openclaw/openclaw)
- Internet connection (for cloud sync)

### Quick Start
```bash
# Run the installer (works on all platforms)
bash ~/.openclaw/skills/amber-hunter/install.sh
```

# Then open https://huper.org/dashboard → "Encryption" tab to set your master password
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create config (get your API key from https://huper.org/dashboard)
mkdir -p ~/.amber-hunter
echo '{"api_key": "your-key", "huper_url": "https://huper.org/api"}' > ~/.amber-hunter/config.json

# Start service
python3 amber_hunter.py &
```

### Get Your API Key
1. Go to [huper.org/dashboard](https://huper.org/dashboard)
2. Login → API Key tab → Generate new key
3. Paste into `~/.amber-hunter/config.json` as `api_key`

---

## Usage

### Freeze via Browser
Open [huper.org](https://huper.org), click "冻结当下" — amber-hunter pre-fills the modal with your current session context and related files.

### Freeze via Terminal
```bash
bash ~/.openclaw/skills/amber-hunter/freeze.sh
```

### Check Status
```bash
curl http://localhost:18998/status
```

---

## API Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/status` | GET | None | Service status |
| `/token` | GET | localhost | Get local API key |
| `/session/summary` | GET | None | OpenClaw conversation summary |
| `/session/files` | GET | None | Recent workspace files |
| `/freeze` | GET/POST | Bearer or ?token= | Trigger freeze |
| `/capsules` | GET | Bearer | List local capsules |
| `/capsules` | POST | Bearer | Create capsule |
| `/capsules/{id}` | GET | Bearer | Get capsule |
| `/capsules/{id}` | DELETE | Bearer | Delete capsule |
| `/sync` | GET | Bearer or ?token= | Sync to cloud |
| `/config` | GET/POST | Bearer or ?token= | Read/set auto_sync config |
| `/recall` | GET | Bearer or ?token= | Retrieve relevant memories, get injection prompts |
| `/master-password` | POST | localhost | Set master password |

## Auto-Sync

When auto-sync is enabled (via Dashboard → Encryption → Auto-sync toggle), every freeze automatically uploads to your huper.org cloud account. Toggle state is stored locally in SQLite — no cloud dependency.

## Proactive Memory Capture

amber-hunter automatically watches your AI collaboration sessions and writes significant moments to amber storage — silently, without you needing to remember to do it.

### Signals Detected

| Signal | Examples |
|--------|---------|
| User correction | "不对", "actually", "错了" |
| Error resolved | command failed → found solution |
| Key decision | architecture, tech stack confirmed |
| User preference | "I prefer...", "I usually..." |
| First success | first time achieving something |

Runs every 10 minutes via LaunchAgent (macOS) or cron/systemd (Linux).

## Active Recall (Proactive Injection)

Before responding to a user message, the AI calls `/recall` to retrieve relevant amber memories and inject them into context — making every reply more informed by past decisions, preferences, and discoveries.

```bash
# Example recall query
curl "http://localhost:18998/recall?q=python%20error&limit=3&token=YOUR_KEY"

# Response includes injected_prompt for each relevant memory
```

**Search modes:**
- `keyword` (default if no vector library) — fast text matching on memo, tags, content
- `semantic` — requires `sentence-transformers` + `numpy`, uses `all-MiniLM-L6-v2` embeddings
- `auto` — uses semantic if available, falls back to keyword

The AI receives pre-formatted memory blocks it can use directly in its reasoning. Response includes `mode` field showing which search mode was used.

---

## Authentication

### Browser Integration (Recommended)
Amber-hunter is designed to work with [huper.org](https://huper.org) via browser. The frontend at huper.org fetches from `localhost:18998` directly — no CORS issues since it's same-origin.

For the freeze button, authentication uses a query parameter to bypass browser restrictions on cross-origin POST requests with custom headers:
```bash
curl "http://localhost:18998/freeze?token=YOUR_API_KEY"
```

### Direct API Calls
```bash
# With Bearer token
curl http://localhost:18998/capsules \
  -H "Authorization: Bearer YOUR_API_KEY"

# With query parameter
curl "http://localhost:18998/capsules?token=YOUR_API_KEY"
```

---

## Security

- **Master Password** stored in OS-native credential store — never written to disk in plaintext
  - macOS: Keychain (via `security` command)
  - Linux: GNOME Keyring (via `secret-tool`)
  - Windows: Credential Manager (via `cmdkey`)
- **Capsules** encrypted with AES-256-GCM before any network transmission
- **API Key** only used for huper.org authentication — not used for encryption
- **Local-first** — works fully offline without cloud sync
- **Zero knowledge** — cloud never sees your master password or unencrypted content

---

## Cross-Platform Support

| OS | Credential Store | Auto-Start | Script |
|----|----------------|-------------|--------|
| macOS | Keychain (`security`) | LaunchAgent | `freeze.sh` (bash) |
| Linux | GNOME Keyring (`secret-tool`) | systemd | `freeze.sh` (bash) |
| Windows | Credential Manager (`cmdkey`) | Task Scheduler | `freeze.ps1` (PowerShell) |

**Linux requirements:** `libsecret-tools` (`apt install libsecret-tools` on Debian/Ubuntu)

---

## File Structure

```
amber-hunter/
├── amber_hunter.py      # FastAPI main service
├── core/
│   ├── crypto.py        # AES-256-GCM encryption
│   ├── db.py            # SQLite local storage
│   ├── keychain.py      # macOS Keychain wrapper
│   ├── models.py        # Pydantic models
│   └── session.py       # OpenClaw session parsing
├── freeze.sh            # Terminal freeze trigger
├── install.sh          # Installation script
└── requirements.txt    # Python dependencies
```

---

## License

MIT License

*Built with 🔒 by [Anke Chen](https://github.com/ankechenlab-node) for the [Huper琥珀](https://huper.org) ecosystem.*

---

## Proactive Memory Capture

amber-hunter includes **amber-proactive** — automatically captures significant moments from your AI collaboration sessions without you needing to remember to do it.

### How It Works

```
AI collaboration session
         ↓
Proactive hook detects signals
         ↓
Automatically writes to amber (silently)
         ↓
Next similar context → AI proactively retrieves relevant memories
```

### Signals Detected

| Signal | Examples | Type |
|--------|---------|------|
| User correction | "不对", "actually", "错了" | `correction` |
| Error resolved | command failed → found solution | `error_fix` |
| Key decision | confirmed architecture/approach | `decision` |
| User preference | "I prefer...", "I usually..." | `preference` |
| First success | first time achieving something | `discovery` |

### Auto-Start (macOS)

```bash
cp ~/.openclaw/skills/amber-hunter/com.huper.amber-proactive.plist \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.huper.amber-proactive.plist
```

Runs every 10 minutes via LaunchAgent, silently.

### Manual Trigger

```bash
node ~/.openclaw/skills/amber-hunter/proactive/scripts/proactive-check.js
tail ~/.amber-hunter/amber-proactive.log
```

### File Structure

```
amber-hunter/
├── amber_hunter.py           # Main FastAPI service
├── core/                     # Core modules (crypto, db, keychain...)
├── proactive/
│   ├── README.md            # Proactive memory documentation
│   ├── hooks/openclaw/      # OpenClaw hook definitions
│   └── scripts/
│       └── proactive-check.js  # Signal detection + amber write
├── freeze.sh               # Terminal freeze trigger
├── install.sh              # Cross-platform installer
└── freeze.ps1             # Windows PowerShell version
```

# gaimode - Google AI Mode Search

**Search Google AI Mode from any OpenClaw agent!**

> ⚠️ Uses Chrome CDP or your Google cookies stored locally. Not affiliated with Google.

---

## Setup

### Option 1: Chrome CDP (Recommended)

**Best for 24/7 reliability!**

```bash
# Start Chrome with debug port
bash ~/start-chrome-cdp.sh

# Keep that Chrome window open!
```

### Option 2: Cookie Method

1. Install [EditThisCookie](https://chrome.google.com/webstore) Chrome extension
2. Go to google.com → Export cookies
3. Save to: `~/.config/gaimode/cookies.json`

---

## Usage

### Check Status
```
exec: python3 ~/.openclaw/workspace/skills/gaimode/gaimode-cli.py status
```

### Search
```
exec: python3 ~/.openclaw/workspace/skills/gaimode/gaimode-cli.py search "PL live score"
exec: python3 ~/.openclaw/workspace/skills/gaimode/gaimode-cli.py search "IPL KKR GT score"
```

---

## CDP Mode Benefits

- ✅ More reliable (connects to YOUR Chrome)
- ✅ No cookie expiration issues
- ✅ Less likely to be blocked by Google
- ✅ 24/7 ready

**Keep Chrome open with debug port running!**

---

## Files

```
gaimode/
├── SKILL.md             # This file
├── gaimode-cli.py       # CLI tool
└── start-chrome-cdp.sh # Chrome CDP launcher
```

---

## License

MIT - See [GitHub](https://github.com/whoisdhana/gaimode-cli)

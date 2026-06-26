# ClawShorts — Block YouTube Shorts on Fire TV

**Set a daily limit. When you hit it, YouTube closes automatically.**

No apps to install on your TV. No accounts needed. Just a daily time limit for YouTube Shorts, enforced on your Fire TV.

---

## What It Does

- Watches how long you watch YouTube Shorts each day
- Closes YouTube when your daily limit is reached
- Resets automatically at midnight
- Works on any Amazon Fire TV / Fire Stick

---

## What You Need

1. A Fire TV or Fire Stick on the same WiFi as your computer
2. Your computer (Mac/Linux) — OpenClaw installed
3. About 5 minutes to set it up

---

## Setup (Step by Step)

### Step 1 — Find Your Fire TV IP

1. On your Fire TV: **Settings → My Fire TV → About → Network**
2. Look for **IP Address** (like `192.168.1.100`)
3. Write it down

### Step 2 — Enable ADB Debugging

1. On your Fire TV: **Settings → My Fire TV → Developer Options**
2. Turn **ON ADB Debugging**

> ⚠️ **Security:** ADB lets your computer control your Fire TV. Only enable this on a **trusted home network**.

### Step 3 — Set It Up

On your computer, run:

```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh setup 192.168.1.100
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh install
```

Replace `192.168.1.100` with your Fire TV's IP address from Step 1.

**That's it.** The daemon starts automatically and will enforce your limit.

---

## Choosing Your Daily Limit

By default, the limit is **300 seconds (5 minutes)** per day.

To change it:

```bash
# 10 minutes per day
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh install 600

# 30 minutes per day
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh install 1800
```

---

## Commands

| What You Want | Command |
|---------------|---------|
| Check today's usage | `~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh status` |
| Reset today's counter | `~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh reset` |
| Stop the limiter | `~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh stop` |
| Start it again | `~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh start` |
| Remove completely | `~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh uninstall` |

---

## How It Works

Every 3 seconds, ClawShorts checks what you're watching:

| What You're Watching | Width | Counts? |
|---------------------|-------|---------|
| YouTube Shorts (vertical video) | ~45% of screen | ✅ Yes |
| Regular YouTube video | ~100% of screen | ❌ No |
| YouTube home screen | varies | ❌ No |
| Fire TV home / other apps | — | ❌ No |

Only actual Shorts playback counts toward your daily limit.

---

## FAQ

**Q: Does this work on Chromecast or smart TV apps?**
A: No — this uses ADB which only works with Fire TV / Android TV.

**Q: Can I use both Fire TV and Fire Stick?**
A: Yes — add both IPs: `~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh setup 192.168.1.100,192.168.1.101`

**Q: Does it block regular YouTube videos?**
A: No — only YouTube Shorts. Regular videos don't count.

**Q: What happens at midnight?**
A: The counter resets automatically. You get your full daily limit back.

**Q: Why do some Shorts not get blocked?**
A: Detection works best when Shorts is the focused element. Brief navigations don't count.

---

## Troubleshooting

**"ADB not found"** — Install ADB on your computer:
```bash
brew install android-platform-tools  # Mac
sudo apt install adb                # Linux
```

**"Daemon not running"** — Start it:
```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh start
```

**Check if it's working:**
```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh status
```

**View logs:**
```bash
tail ~/.clawshorts/daemon.log
```

---

## Uninstall

```bash
~/.openclaw/workspace/skills/clawshorts/scripts/clawshorts.sh uninstall
```

This removes the auto-start daemon but keeps your usage data.

---

## Files & Data

- `~/.clawshorts/` — all data lives here
- `~/.clawshorts/clawshorts.db` — your watch history
- `~/.clawshorts/daemon.log` — debug log
- `~/Library/LaunchAgents/com.fink.clawshorts.plist` — auto-start (macOS)

---

ClawShorts © 2026 — MIT License

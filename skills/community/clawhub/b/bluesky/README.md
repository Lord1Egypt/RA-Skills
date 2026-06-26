# 🦋 Bluesky CLI

[![Version](https://img.shields.io/badge/version-1.6.3-blue.svg)](https://github.com/jeffaf/bluesky-skill)
[![License](https://img.shields.io/badge/license-MIT--0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://python.org)

A full-featured command-line interface for [Bluesky](https://bsky.app) (AT Protocol). Post, reply, like, repost, follow, block, mute, search — everything you need to engage on Bluesky from your terminal.

**Built for [OpenClaw](https://github.com/openclaw/openclaw)** — works standalone too.

## ✨ Features

| Category | Commands |
|----------|----------|
| **Content** | `post`, `reply`, `quote`, `delete` |
| **Engagement** | `like`, `unlike`, `repost`, `unrepost` |
| **Social** | `follow`, `unfollow`, `profile` |
| **Moderation** | `block`, `unblock`, `mute`, `unmute` |
| **Discovery** | `timeline`, `search`, `notifications`, `thread` |
| **Threading** | `create-thread` — post multi-part threads |
| **Media** | Image attachments with alt text |

**Plus:** JSON output on all read commands, dry-run mode, auto-linked URLs and @mentions.

## 🚀 Quick Start

### Step 1: Get an App Password from Bluesky

1. Open [bsky.app](https://bsky.app) and log in
2. Click your avatar → **Settings**
3. Go to **Privacy and Security** → **App Passwords**
4. Click **Add App Password**
5. Name it something like "CLI" or "OpenClaw"
6. Keep the generated password ready for the CLI prompt

> ⚠️ **Do not paste app passwords into chat, shell history, or command-line arguments.** Bluesky only shows the password once, so use it in the hidden prompt and store/revoke it from Bluesky settings as needed.

### Step 2: Login via CLI

Run locally:
```bash
bsky login --handle yourname.bsky.social
```

The CLI prompts for the app password without echoing it. Your password is used once to get a session token, then immediately discarded. It's never stored.

Legacy `--password` still works for backward compatibility, but it is intentionally hidden from help and prints a warning because command-line secrets can leak.

### Step 3: Verify & Start Posting

```bash
bsky whoami                              # Confirm you're logged in
bsky post "Hello from the command line! 🦋"  # Your first post!
```

## 📖 Usage

### Posting & Content

```bash
bsky post "Hello world!"                              # Simple post
bsky post "Look!" --image pic.jpg --alt "A sunset"    # With image
bsky reply <url> "Great point!"                       # Reply
bsky quote <url> "This is important"                  # Quote-post
bsky delete <url> --yes                               # Delete after verifying target
```

### Engagement

```bash
bsky like <url>          # ❤️ Like a post
bsky unlike <url>        # Remove like
bsky repost <url> --yes   # 🔁 Boost after verifying target
bsky unrepost <url> --yes # Remove repost after verifying target
```

### Social

```bash
bsky follow @someone.bsky.social --yes    # Follow after verifying target
bsky unfollow @someone.bsky.social --yes  # Unfollow after verifying target
bsky profile @someone.bsky.social         # View profile
```

### Moderation

```bash
bsky block @troll.bsky.social --yes       # 🚫 Block after verifying target
bsky unblock @someone.bsky.social --yes   # Unblock after verifying target
bsky mute @noisy.bsky.social --yes        # 🔇 Mute after verifying target
bsky unmute @someone.bsky.social --yes    # Unmute after verifying target
```

### Threading

```bash
bsky create-thread "First post" "Second post" "Third post"   # Create a thread
bsky ct "Post 1" "Post 2" "Post 3"                           # Short alias
bsky create-thread "Intro" "Details" --dry-run                # Preview only
bsky create-thread "Look!" "More" --image pic.jpg --alt "Photo"  # Image on first post
```

### Discovery

```bash
bsky timeline                       # Your home feed
bsky timeline -n 30                 # More posts
bsky search "topic"                 # Search posts
bsky notifications                  # Your notifications
bsky thread <url>                   # View conversation
```

### JSON Output

Add `--json` to any read command for structured output:

```bash
bsky timeline --json | jq '.[0].text'
bsky search "AI" --json
bsky notifications --json
```

## 🔒 Security

- **Password never stored** — used once to get a session token, then discarded
- **Safe login guidance** — documented login uses a hidden prompt; legacy `--password` is hidden and warns if used
- **Optional confirmation gates** — set `BSKY_CONFIRM_MUTATIONS=1` to make delete, repost/unrepost, follow/unfollow, block/unblock, and mute/unmute prompt unless `--yes` is supplied
- **Session tokens auto-refresh** — no need to re-login
- **Config file permissions** — 600 (owner-only read/write)
- **Location:** `~/.config/bsky/config.json`

## 📦 Installation

### For OpenClaw

```bash
openclaw skills install bluesky
```

### Manual

```bash
git clone https://github.com/jeffaf/bluesky-skill.git ~/clawd/skills/bluesky
cd ~/clawd/skills/bluesky/scripts
./bsky --version  # Auto-creates venv on first run
```

### Requirements

- Python 3.8+
- `atproto` package (installed automatically on first run via venv)

## 🎯 Tips

- **Handles:** Leading `@` is optional; use the full handle, such as `alice.bsky.social`
- **URLs:** Both `https://bsky.app/...` and `at://` URIs work
- **Dry run:** Use `--dry-run` on post/reply/quote to preview
- **Account changes:** Verify targets first; use `--yes` when opt-in confirmations are enabled
- **Images:** Max 1MB, alt text required (accessibility)

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📄 License

MIT-0 — do whatever you want with it.

---

Made with 🦞 by [jeffaf](https://github.com/jeffaf) and [Mai](https://github.com/openclaw/openclaw)

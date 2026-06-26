# 🛠️ EduClaw Setup Guide — Full Installation

> Step-by-step guide to set up **EduClaw IELTS Study Planner** from scratch, including OpenClaw, Google Calendar, Google AI (Gemini), Discord bot, Telegram bot, web search, and SQLite.

**[🇻🇳 Đọc bằng Tiếng Việt](SETUP_VI.md)**

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install OpenClaw](#2-install-openclaw)
3. [Google Cloud Setup (API Keys)](#3-google-cloud-setup)
4. [Configure OpenClaw with API Key](#4-configure-openclaw-with-api-key)
5. [Install & Authenticate gcalcli (Google Calendar)](#5-install--authenticate-gcalcli)
6. [Enable Web Search](#6-enable-web-search)
7. [Create & Connect Discord Bot](#7-create--connect-discord-bot)
8. [Create & Connect Telegram Bot (Optional)](#8-create--connect-telegram-bot-optional)
9. [Install SQLite](#9-install-sqlite)
10. [Install EduClaw Skill](#10-install-educlaw-skill)
11. [Start OpenClaw Gateway](#11-start-openclaw-gateway)
12. [Verification Checklist](#12-verification-checklist)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Prerequisites

| Requirement | Minimum |
|------------|---------|
| **OS** | Linux (Ubuntu/Debian recommended), macOS, or WSL2 |
| **Node.js** | v20+ (`node --version`) |
| **Python** | 3.10+ (`python3 --version`) |
| **pip** | Latest (`pip3 --version`) |
| **Git** | Any recent version |
| **Google Account** | For Calendar + AI API |

---

## 2. Install OpenClaw

### Option A: One-line install (recommended)

```bash
curl -fsSL https://get.openclaw.dev | bash
```

### Option B: npm global install

```bash
npm install -g openclaw
```

### Verify installation

```bash
openclaw --version
# Should output: OpenClaw 2026.x.x
```

### Initialize OpenClaw

```bash
openclaw config
```

This runs the setup wizard. It will:
- Create `~/.openclaw/` directory
- Prompt for model provider and API key
- Set up basic config

You can re-run the wizard anytime:
```bash
openclaw config          # Full wizard
openclaw doctor          # Check for issues
```

---

## 3. Google Cloud Setup

EduClaw needs two Google API keys:
1. **Gemini API Key** — for the AI model (Gemini 2.5/3.x)
2. **Google Calendar OAuth** — for gcalcli to read/write calendar events

### 3.1. Get Gemini API Key (for AI model)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Select or create a Google Cloud project
4. Copy the API key (starts with `AIzaSy...`)
5. **Important:** Check your [billing/quota](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas) — free tier has rate limits. Increase spending cap if needed.

> **Save this key** — you'll need it in Step 4.

### 3.2. Enable Google Calendar API

1. Go to [Google Cloud Console → APIs & Services](https://console.cloud.google.com/apis/library)
2. Search for **"Google Calendar API"**
3. Click **Enable**
4. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
5. Click **"+ CREATE CREDENTIALS" → "OAuth client ID"**
6. If prompted, configure the **OAuth consent screen** first:
   - User Type: **External** (or Internal if using Google Workspace)
   - App name: e.g., `EduClaw Calendar`
   - User support email: your email
   - Scopes: add `https://www.googleapis.com/auth/calendar`
   - Test users: add your own email
   - Save
7. Back in Credentials → **"+ CREATE CREDENTIALS" → "OAuth client ID"**:
   - Application type: **Desktop app**
   - Name: e.g., `gcalcli`
   - Click **Create**
8. Download the **JSON file** (client secret) — you'll need it for gcalcli

> **Keep this JSON file** — you'll use it in Step 5.

### 3.3. Get Web Search API Key (optional but recommended)

EduClaw uses web search to find study materials. Two options:

#### Option A: Use Gemini's built-in search (easiest)
If your Gemini API key has search grounding enabled, you can use the same key. Skip to Step 6.

#### Option B: Google Custom Search API
1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all)
2. Create a new search engine → search the entire web
3. Copy the **Search Engine ID (cx)**
4. Go to [Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) → **Enable**
5. Create an API key for it (or use your existing one)

---

## 4. Configure OpenClaw with API Key

### Option A: Via setup wizard

```bash
openclaw config
# Select "google" as provider
# Paste your Gemini API key when prompted
```

### Option B: Manual config

```bash
# Set the AI model provider and key
openclaw config set auth.profiles.google:default.provider google
openclaw config set auth.profiles.google:default.mode api_key
```

Then edit `~/.openclaw/agents/main/agent/auth-profiles.json`:
```json
{
  "version": 1,
  "profiles": {
    "google:default": {
      "type": "api_key",
      "provider": "google",
      "key": "YOUR_GEMINI_API_KEY_HERE"
    }
  }
}
```

### Configure model preferences

Edit `~/.openclaw/openclaw.json` → `agents.defaults.model`:
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3-flash-preview",
        "fallbacks": [
          "google/gemini-2.5-flash",
          "google/gemini-2.5-pro"
        ]
      }
    }
  }
}
```

### Verify model works

```bash
openclaw agent --message "Hello, respond with just 'OK'"
# Should get a response from the model
```

---

## 5. Install & Authenticate gcalcli

gcalcli is a command-line interface for Google Calendar.

### Install

```bash
pip3 install gcalcli
```

> If you get `externally-managed-environment` error on Ubuntu 24+:
> ```bash
> pip3 install --break-system-packages gcalcli
> # OR use pipx:
> pipx install gcalcli
> ```

### Authenticate with OAuth

#### Method A: Using the client secret JSON from Step 3.2

```bash
gcalcli --client-id /path/to/client_secret.json list
```

This opens a browser for OAuth consent. Sign in with your Google account and authorize.

#### Method B: First run (default credentials)

```bash
gcalcli list
```

On first run, gcalcli will:
1. Open a browser window
2. Ask you to sign in to Google
3. Ask permission to access your calendar
4. Save credentials locally (~/.gcalcli_oauth)

### Verify

```bash
gcalcli --nocolor list
# Should show your calendars, e.g.:
#  owner  moclaw128@gmail.com
#  reader Holidays in Viet Nam
```

```bash
gcalcli --nocolor agenda
# Should show upcoming events (or empty if no events)
```

### Specify calendar (if you have multiple)

```bash
gcalcli --calendar "moclaw128@gmail.com" agenda
```

---

## 6. Enable Web Search

Web search lets EduClaw find IELTS study materials automatically.

### Using Gemini search grounding (recommended)

Edit `~/.openclaw/openclaw.json`:
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "gemini",
        "gemini": {
          "apiKey": "YOUR_WEB_SEARCH_API_KEY_HERE"
        }
      }
    }
  }
}
```

> You can use the same Gemini API key if it supports search grounding, or a separate key for web search.

### Verify

```bash
openclaw agent --message "Search the web for 'IELTS Listening tips 2026' and give me 3 links"
# Should return real URLs from web search
```

---

## 7. Create & Connect Discord Bot

### 7.1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name it (e.g., `Jaclyn`, `EduClaw Bot`, or any name you want)
4. Go to **"Bot"** tab on the left
5. Click **"Reset Token"** → **Copy the bot token** (you'll need it below)
6. Under **Privileged Gateway Intents**, enable:
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent** (optional)
   - ✅ **Presence Intent** (optional)

### 7.2. Generate Invite Link

1. Go to **"OAuth2" → "URL Generator"**
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Embed Links
   - ✅ Use Slash Commands
   - ✅ Send Messages in Threads
   - ✅ Manage Messages (optional, for cleanup)
4. Copy the generated URL
5. Open it in your browser → select your Discord server → **Authorize**

### 7.3. Connect to OpenClaw

```bash
openclaw channels add \
  --channel discord \
  --token "YOUR_DISCORD_BOT_TOKEN_HERE" \
  --name "Jaclyn"
```

Or edit `~/.openclaw/openclaw.json` directly:
```json
{
  "channels": {
    "discord": {
      "name": "Jaclyn",
      "enabled": true,
      "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
      "groupPolicy": "open",
      "streaming": "partial"
    }
  }
}
```

### 7.4. Restart gateway & verify

```bash
systemctl --user restart openclaw-gateway
# Or if not using systemd:
openclaw gateway
```

```bash
openclaw channels status
# Should show Discord: connected
```

### 7.5. Deploy slash commands

```bash
openclaw directory self --channel discord
```

This deploys slash commands to Discord (e.g., `/educlaw_ielts_planner`, `/help`, etc.)

### 7.6. Test

- Open Discord
- DM your bot or mention it in server: `@Jaclyn hello`
- Should get a response

### 7.7. Fix "not authorized" in server channels

If slash commands work in DM but show "not authorized" in a server:

1. Go to **Server Settings → Integrations**
2. Find your bot → click **"Manage"**
3. Enable the commands for your desired channels/roles
4. Make sure the bot has permission to send messages and use slash commands in the channel

---

## 8. Create & Connect Telegram Bot (Optional)

### 8.1. Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g., `EduClaw Bot`)
4. Choose a username (must end in `bot`, e.g., `educlaw_ielts_bot`)
5. **Copy the bot token** that BotFather gives you (format: `1234567890:ABCdefGHIjklmNOPqrs...`)

### 8.2. Configure bot settings (optional)

Send these commands to @BotFather:
```
/setdescription    → "Personal IELTS Study Secretary"
/setabouttext      → "EduClaw helps you plan and track IELTS study with Google Calendar integration"
/setcommands       → plan - Plan IELTS study
                     progress - Check study progress
                     schedule - Schedule next 2 weeks
```

### 8.3. Connect to OpenClaw

```bash
openclaw channels add \
  --channel telegram \
  --token "YOUR_TELEGRAM_BOT_TOKEN_HERE" \
  --name "EduClaw"
```

Or edit `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "telegram": {
      "name": "EduClaw",
      "enabled": true,
      "token": "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    }
  }
}
```

### 8.4. Restart & verify

```bash
systemctl --user restart openclaw-gateway
openclaw channels status
# Should show Telegram: connected
```

### 8.5. Test

- Open Telegram
- Search for your bot (by username)
- Send: `Lên kế hoạch IELTS 7.5`
- Should get a response

---

## 9. Install SQLite

EduClaw uses SQLite for progress tracking.

### Ubuntu/Debian

```bash
sudo apt install -y sqlite3
```

### macOS

```bash
# sqlite3 is pre-installed on macOS
sqlite3 --version
```

### Verify

```bash
sqlite3 --version
# Should output: 3.x.x ...

# Also verify Python sqlite3 module
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

---

## 10. Install EduClaw Skill

### From OpenClaw registry (when available)

```bash
openclaw skill install educlaw-ielts-planner
```

### Manual installation

```bash
git clone https://github.com/moclaw/educlaw-ielts-planner.git
cp -r educlaw-ielts-planner/* ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/
```

### Initialize the SQLite database

```bash
mkdir -p ~/.openclaw/workspace/tracker
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db \
  < ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/schema.sql
```

### Verify skill is loaded

```bash
openclaw skill list
# Should show: educlaw-ielts-planner  1.0.0  ✓ loaded
```

---

## 11. Start OpenClaw Gateway

### Option A: Systemd service (recommended for always-on)

```bash
# Enable and start the gateway as a user service
openclaw gateway install-service
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway
```

Check status:
```bash
systemctl --user status openclaw-gateway
# Should show: active (running)
```

### Option B: Run in foreground

```bash
openclaw gateway
```

### Option C: Run in background with nohup

```bash
nohup openclaw gateway &
```

---

## 12. Verification Checklist

Run through this checklist to confirm everything works:

```bash
# 1. OpenClaw version
openclaw --version

# 2. Model API works
openclaw agent --message "Say OK"

# 3. Google Calendar
gcalcli --nocolor list

# 4. Web search
openclaw agent --message "Search web for 'IELTS tips' and give me one link"

# 5. Discord connected (if configured)
openclaw channels status

# 6. SQLite ready
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db ".tables"
# Should output: materials  sessions  vocabulary  weekly_summaries  + views

# 7. Skill loaded
openclaw skill list | grep educlaw

# 8. Gateway running
systemctl --user status openclaw-gateway

# 9. Test EduClaw
openclaw agent --message "Plan my IELTS study for band 7.5"
# OR via Discord DM: @Jaclyn Plan my IELTS study
```

| # | Check | Expected Result |
|---|-------|----------------|
| 1 | `openclaw --version` | `OpenClaw 2026.x.x` |
| 2 | Model response | AI responds "OK" |
| 3 | `gcalcli list` | Shows your calendars |
| 4 | Web search | Returns real URLs |
| 5 | Channel status | Discord: connected |
| 6 | SQLite tables | 4 tables + 5 views |
| 7 | Skill loaded | `educlaw-ielts-planner ✓` |
| 8 | Gateway status | `active (running)` |
| 9 | EduClaw test | Asks for study preferences |

---

## 13. Troubleshooting

### Model returns 429 / RESOURCE_EXHAUSTED

Your Gemini API key has hit the spending cap.

**Fix:** Go to [Google Cloud Console → Billing](https://console.cloud.google.com/billing) → increase the spending cap for the Generative Language API.

### gcalcli: "Unable to authenticate"

OAuth token expired or credentials file missing.

**Fix:**
```bash
rm -f ~/.gcalcli_oauth
gcalcli list   # Re-authenticate
```

### Discord bot not responding

1. Check gateway is running: `systemctl --user status openclaw-gateway`
2. Check channel status: `openclaw channels status`
3. Check logs: `openclaw channels logs --channel discord | tail -20`
4. Verify bot token is correct in `openclaw.json`
5. Make sure **Message Content Intent** is enabled in Discord Developer Portal

### "not authorized" for slash commands in server

Go to **Server Settings → Integrations → Your Bot → Manage** → enable commands for the channel.

### SQLite: "unable to open database"

```bash
# Make sure the directory exists
mkdir -p ~/.openclaw/workspace/tracker
# Re-create the database
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db \
  < ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/schema.sql
```

### Web search not working

1. Check config: `openclaw config get tools.web.search`
2. Verify API key in `openclaw.json` → `tools.web.search.gemini.apiKey`
3. Make sure the API is enabled in Google Cloud Console

### pip install error: "externally-managed-environment"

Ubuntu 24+ blocks global pip installs.

**Fix:**
```bash
pip3 install --break-system-packages gcalcli
# OR
pipx install gcalcli
```

### Cron jobs not sending Discord messages

1. Check cron list: `openclaw cron list`
2. Test a job: `openclaw cron run ielts-daily-prep`
3. Check logs: `openclaw channels logs --channel discord | tail -30`
4. Verify gateway is running and Discord is connected

---

## Quick Start Summary

```bash
# 1. Install OpenClaw
curl -fsSL https://get.openclaw.dev | bash

# 2. Run setup wizard (configures API key + model)
openclaw config

# 3. Install gcalcli + authenticate
pip3 install gcalcli
gcalcli list

# 4. Connect Discord bot
openclaw channels add --channel discord --token "BOT_TOKEN" --name "Jaclyn"

# 5. Install EduClaw skill
git clone https://github.com/moclaw/educlaw-ielts-planner.git
cp -r educlaw-ielts-planner/* ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/

# 6. Init database + start
mkdir -p ~/.openclaw/workspace/tracker
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db \
  < ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/schema.sql
systemctl --user restart openclaw-gateway

# 7. Test!
openclaw agent --message "Plan my IELTS study for band 7.5"
```

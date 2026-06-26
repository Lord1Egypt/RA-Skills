---
name: ai-director
description: AI short drama generation - account management, script writing, video production. Integrated X2C billing for commercial deployment.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["node"], "env": ["X2C_API_KEY"] },
        "primaryEnv": "X2C_API_KEY",
      },
  }
---

# AI Director - AI Short Drama Generation

Complete AI short drama solution — from concept to finished film, with integrated X2C platform account management and billing.

## Multi-User Support

Each user has independent X2C credentials stored in `credentials/{USER_ID}.json`.

Set `USER_ID` or `TELEGRAM_USER_ID` env var when calling scripts:

```bash
USER_ID=12345 node {baseDir}/scripts/ad-account-manager.js check-binding
```

OpenClaw passes the user ID automatically from chat context.

## Modules

### 1. Ad Account Manager

X2C platform account binding and verification.

```bash
# Send verification code
node {baseDir}/scripts/ad-account-manager.js send-code user@example.com

# Verify and get API Key
node {baseDir}/scripts/ad-account-manager.js verify user@example.com 123456

# Check binding status
node {baseDir}/scripts/ad-account-manager.js check-binding

# View config options
node {baseDir}/scripts/ad-account-manager.js config

# Unbind account
node {baseDir}/scripts/ad-account-manager.js unbind

# Direct bind with existing key
node {baseDir}/scripts/ad-account-manager.js bind --key "x2c_sk_xxx"
```

### 2. Ad Character Manager

Manage custom characters for video production. Max 5 per user.

```bash
node {baseDir}/scripts/ad-character-manager.js list
node {baseDir}/scripts/ad-character-manager.js create <name> <gender> <image_url>
node {baseDir}/scripts/ad-character-manager.js delete <character_id>
```

| Param     | Required | Options               |
| --------- | :------: | --------------------- |
| name      |   Yes    | Display name          |
| gender    |   Yes    | male, female, other   |
| image_url |   Yes    | Public URL (max 10MB) |

### 3. Ad Writer (Prompt Engineering)

Agent reads `references/AD-WRITER-GUIDE.md` and generates a complete script based on user's creative concept. Outputs: title, synopsis, character bios, outline, episode breakdowns, full screenplay.

### 4. Ad Producer (Video Production)

```bash
# View pricing and config
node {baseDir}/scripts/ad-producer.js config

# Generate script
node {baseDir}/scripts/ad-producer.js generate-script "your concept" --wait

# Check script status
node {baseDir}/scripts/ad-producer.js script-status <project_id>

# Produce video
node {baseDir}/scripts/ad-producer.js produce-video <project_id> 1 --wait

# Check video progress
node {baseDir}/scripts/ad-producer.js video-status <project_id> 1

# Full workflow (recommended)
node {baseDir}/scripts/ad-producer.js full-workflow "your concept" --duration 120
```

### Generation Options

| Param           | Description                          | Default     |
| --------------- | ------------------------------------ | ----------- |
| --mode          | short_video / short_drama            | short_video |
| --duration      | 60 / 120 / 180 / 300                 | 120         |
| --ratio         | 9:16 / 16:9                          | 9:16        |
| --style         | Style name                           | -           |
| --episodes      | Fixed: short_video=1, short_drama=10 | -           |
| --language      | zh / en                              | zh          |
| --character-ids | Character UUIDs (comma-separated)    | -           |
| --wait          | Wait for completion                  | false       |

### Cost

| Item                 | Credits | USD   |
| -------------------- | ------- | ----- |
| Script (short_video) | 6       | $0.06 |
| Script (short_drama) | 60      | $0.60 |
| Video 60s            | 299     | $2.99 |
| Video 120s           | 599     | $5.99 |
| Video 180s           | 799     | $7.99 |
| Video 300s           | 999     | $9.99 |

## Quality Evaluator

Uses Gemini to score video quality against defined criteria.

```bash
node {baseDir}/scripts/quality-evaluator.js <video_url> --prompt "original prompt"
node {baseDir}/scripts/quality-evaluator.js <video_url> --json
```

Requires `GEMINI_API_KEY` env var or `geminiApiKey` in config.

## Auto-Iterate

Automatically evaluate + improve prompt + regenerate until quality threshold met.

```bash
node {baseDir}/scripts/auto-iterate.js "your concept" \
  --duration 60 --style "style" --threshold 80 --max-iterations 5
```

## Critical Rules

- Confirm all parameters with user before generating video
- Only use values from config options (styles, categories) — never custom values
- Episodes are fixed: short_video=1, short_drama=10
- Each episode can only be submitted once for production
- Never auto-retry failed generations (costs credits)
- Use async task handling — do not block with --wait in production
- Output video URLs completely, never truncate
- Remove `&response-content-disposition=attachment` from video URLs for browser playback

## API Reference

See `references/X2C-OPEN-API.md` for complete API documentation.

## Credentials

Store in `credentials/{USER_ID}.json`:

```json
{
  "x2cApiKey": "x2c_sk_xxx",
  "x2cEmail": "your@email.com",
  "x2cUserId": "user-uuid"
}
```

Or set `X2C_API_KEY` env var, or configure via `skills."ai-director".env.X2C_API_KEY` in `~/.openclaw/openclaw.json`.

---
name: ai-code-review
version: 1.1.0
description: Automated code review with LLM analysis, voice transcription, and Discord notifications
author: openclaw
tags: [code-review, llm, whisper, discord, automation]
---

# AI Code Review Skill

Automated code review service that combines LLM-powered diff analysis, voice-note transcription, and Discord notifications into a unified review pipeline.

## Features

- **LLM Code Analysis**: Sends diffs to GPT-4o with structured JSON output (issues count, suggestions, approval status, summary)
- **Voice Note Transcription**: Transcribes review meeting recordings via OpenAI Whisper API with file validation
- **Discord Notifications**: Rich embed notifications with approval status, issue counts, and color-coded indicators
- **URL Safety**: Scheme validation prevents SSRF attacks on all fetched URLs
- **Request Timeouts**: All HTTP calls enforce a 30-second timeout to prevent hanging
- **Structured Logging**: Consistent logging throughout with `logging` module
- **ClawHub Publishing**: Built-in `publish_skill()` helper using the ClawHub CLI

## Quick Start

```bash
# Set required environment variables
export OPENAI_API_KEY="sk-..."
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."  # optional

# Run a review
python src/code_review_service.py
```

## API Reference

### `process_pull_request(pr_number, diff_url, voice_note_path=None)`

End-to-end PR review: fetches diff, runs LLM analysis, optionally transcribes a voice note, and sends a Discord notification.

Returns a dict with keys: `issues_found`, `suggestions`, `approval`, `summary`, and optionally `voice_note_transcription`.

### `analyze_code_changes(diff_content)`

Sends diff text to GPT-4o for analysis. Returns structured JSON with `issues_found`, `suggestions`, `approval` (approved/needs_changes/rejected), and `summary`.

### `transcribe_voice_note(audio_file_path)`

Validates the audio file exists and is non-empty, then transcribes via Whisper-1. Returns the transcription text.

### `send_discord_notification(message, embed=None)`

Posts a message (with optional rich embed) to the configured Discord webhook. Returns `True` on success.

### `publish_skill(skill_path, version)`

Publishes a skill directory to ClawHub at the given version using the `clawhub` CLI.

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key for GPT-4o and Whisper |
| `DISCORD_WEBHOOK_URL` | No | — | Discord webhook URL for notifications |
| `CLAWHUB_API_URL` | No | `https://api.clawhub.com/v1` | ClawHub API base URL |

## Health Check

The included `scripts/healthcheck.sh` monitors nginx, docker, code-review-service, and whisper-api-gateway. It auto-restarts failed services and sends Discord alerts. Disk usage warnings trigger at 80% and critical alerts at 90%.

## Changelog

### 1.1.0
- Fixed SSRF vulnerability: added `_validate_url()` with scheme allowlist for all fetched URLs
- Added 30-second request timeouts to all `requests` calls (diff fetch + Discord webhook)
- Replaced bare `except` clauses with specific exception types (`requests.RequestException`, `FileNotFoundError`, `ValueError`, `json.JSONDecodeError`)
- Added input validation: file existence/size checks for audio, empty-diff handling
- Implemented actual LLM-based code analysis via GPT-4o (replaced stub `analyze_code_changes`)
- Added `logging` module throughout; removed silent error swallowing
- Lazy-initialized OpenAI client with clear error on missing key
- Improved error handling in voice note transcription (graceful skip on failure)
- Enhanced health check script compatibility with chroot/container environments

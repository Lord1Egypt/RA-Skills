# AI Code Review

Automated code review powered by LLM analysis, voice-note transcription, and Discord notifications.

## Features

- LLM-based code diff analysis with structured JSON output
- Voice note transcription via OpenAI Whisper
- Discord webhook notifications with rich embeds
- Health monitoring and service checks
- ClawHub skill publishing

## Usage

```bash
# Run a code review
python src/code_review_service.py
```

## Configuration

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `DISCORD_WEBHOOK_URL` | No | Discord webhook for notifications |
| `CLAWHUB_API_URL` | No | ClawHub API base URL |

## Changelog

### 1.1.0
- Fixed SSRF vulnerability in URL fetching (added scheme validation)
- Added request timeouts to all HTTP calls
- Replaced bare `except` with specific exception handling
- Added input validation for file paths and empty inputs
- Implemented actual LLM-based code analysis (replaced stub)
- Added proper logging throughout the service
- Added lazy-initialized OpenAI client
- Improved error handling in voice note transcription
- Enhanced health check script compatibility

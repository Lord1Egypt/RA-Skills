# ai-code-review

AI-powered code review service with voice transcription, Discord notifications, and ClawHub integration.

## Triggers

- "code review", "review code", "PR review"
- "transcribe voice note", "voice review"
- "publish skill", "skill publish"

## Usage

### Review a pull request

```bash
python src/code_review_service.py <pr_number> <diff_url> [voice_note_path]
```

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key for Whisper transcription |
| `DISCORD_WEBHOOK_URL` | No | Discord webhook for review notifications |
| `VOICE_NOTE_BASE_DIR` | No | Base directory for voice note files (default: `/tmp/voice_notes`) |
| `ALLOW_INTERNAL_DIFF_URLS` | No | Set to allow internal-network diff URLs (security override) |

## Security

- Diff URLs are validated against SSRF (scheme + hostname checks)
- Voice note paths are sandboxed to `VOICE_NOTE_BASE_DIR`
- Discord notification content is escaped to prevent injection
- All HTTP requests enforce a 30-second timeout

## Changelog

### 1.1.0 (2026-05-07)

- Fixed SSRF vulnerability in diff URL fetching
- Fixed path traversal risk in voice note transcription
- Added Discord content escaping to prevent injection
- Added request timeouts (30s) to all HTTP calls
- Fixed `analyze_code_changes` returning hardcoded "approved" — now returns "pending_manual_review"
- Added proper error handling for diff fetch and voice transcription
- Added structured logging throughout the service
- Improved `__main__` with CLI arg parsing and error handling
- Optimized health check script compatibility (works in chroot/container environments)
# Changelog

## [2.1.6] - 2026-03-03

### Changed
- Hardened API key handling and synced OpenClaw metadata/docs.


## [2.1.5] - 2026-02-11

### Changed
- **API Key Loading:** Simplified to only read from environment variable (`ELEVEN_API_KEY` / `ELEVENLABS_API_KEY`) or skill-local `.env` file
- **Removed:** No longer probes `~/.openclaw/openclaw.json` for API key
- **Note:** This is a breaking change if you relied on the OpenClaw config file for the API key. Use environment variables instead.

## [2.1.3] - 2026-02-04

- Privacy cleanup: removed hardcoded paths and personal info from docs

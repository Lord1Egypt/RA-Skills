# Changelog

## [2.2.0] - 2026-08-31

### Fixed
- The OpenClaw TTS example configured a `tts.elevenlabs` block. No such key exists; provider settings live under `tts.providers.<name>`. Following the old example left built-in TTS unconfigured.
- Documented that OpenClaw built-in TTS reads `ELEVENLABS_API_KEY` or `XI_API_KEY`, while this skill's scripts read `ELEVEN_API_KEY`. The two paths are independent.
- `requires.env` was an object (`{"ELEVEN_API_KEY": "required"}`). OpenClaw expects a string array and drops anything else. Replaced with `envVars`.
- Removed `package.json`. It declared an npm package that was never published and had no `main`, dependencies, or scripts. ClawHub CLI 0.22+ refuses to publish any folder containing a `package.json` as a skill.

### Note
- OpenClaw cannot express "one of two environment variables". The skill therefore loads without a key and the scripts fail on the first call if neither variable is set.

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

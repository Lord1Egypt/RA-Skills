# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-03-27

### Added
- `gemini-worker/SKILL.md` — OpenClaw skill definition with headless worker pattern
- `gemini-worker/references/acp-vs-headless.md` — Technical deep dive: why `gemini --acp`
  fails headlessly and why `gemini -p --yolo` works. Includes decision matrix and concept
  for a future ACP harness.
- `gemini-worker/references/prompt-patterns.md` — Reusable prompt templates:
  - Anthropic fallback (drop-in replacement for 529 errors)
  - Validation/review pattern
  - Dev agent pattern
  - File-write pattern (avoid stdout truncation)
  - Deep analysis pattern
  - Batch processing pattern
  - Code review pattern
  - Pre-fetch helper (workaround for WebFetchTool headless unreliability)
- `gemini-worker/references/troubleshooting.md` — Common errors with causes and fixes
- `gemini-worker/scripts/gemini-run.sh` — Wrapper script with timeout, logging, and
  validation

### Origin

Discovered during an Anthropic API outage on 2026-03-27. Both `claude-opus-4-6` and
`claude-sonnet-4-6` returned `529 Overloaded` for hours. While pivoting to Gemini CLI as
a fallback, we discovered:

1. `gemini --acp` requires a TTY and hangs headlessly
2. `gemini -p "..." --yolo` works perfectly headlessly
3. `--include-directories` is required to access files outside Gemini's workspace

This skill documents that pattern so others don't have to rediscover it.

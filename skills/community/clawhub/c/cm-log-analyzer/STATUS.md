# log-analyzer — Status

**Status:** Ready
**Price:** $69
**Built:** 2026-03-28

## Description
Parse application logs into actionable error digests with pattern grouping, severity classification, trend detection, and remediation recommendations. Supports 8+ log formats with auto-detection.

## Features
- Auto-detect 8+ log formats (JSON, syslog, Apache, Nginx, Python traceback, Docker, etc.)
- 15+ known error pattern matchers with specific remediation advice
- Message normalization and fingerprinting for pattern grouping
- Hourly trend detection
- 3 output formats: text, JSON, markdown
- CI-friendly exit codes
- Time filtering, severity filtering, pattern ignoring

## Files
- `SKILL.md` — Main skill instructions
- `scripts/analyze_logs.py` — Core analyzer script (Python 3, stdlib only)
- `references/error-patterns.md` — Detailed error pattern reference catalog

## Testing
- Tested against mixed timestamped logs ✅
- Tested against JSON structured logs (Bunyan/Winston-style) ✅
- Tested against Python traceback logs ✅
- Tested directory scanning (multiple files) ✅
- Tested all 3 output formats (text, JSON, markdown) ✅
- Tested against real system logs ✅

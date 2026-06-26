# env-config-validator — Status

**Status:** Ready
**Price:** $49
**Built:** 2026-03-30

## Features
- 12 common mistake detectors (placeholders, trailing spaces, invalid ports, etc.)
- Schema validation with type checking, required vars, patterns, ranges
- Environment diff (dev vs prod) with secret masking
- Auto-generate schema from existing .env
- 3 output formats (text, JSON, markdown)
- CI-friendly exit codes
- Handles export prefix, quoted values, comments

## Tested
- Common checks with 15 detected issues
- Schema generation and validation
- Environment diff with secret masking
- JSON and markdown output
- Severity filtering
- Edge cases (empty values, duplicates, inline comments)

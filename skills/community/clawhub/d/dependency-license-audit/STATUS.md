# dependency-license-audit — Status

**Price:** $69
**Status:** Ready
**Created:** 2026-03-29

## Features
- 5 ecosystem support: npm, pip, Go, Rust, Ruby
- 4 built-in policies: permissive, weak-copyleft, any-open, custom
- Custom policy via .license-policy.json (allowed/blocked lists + exceptions)
- 80+ license aliases → SPDX normalization
- SPDX expression support (OR/AND evaluation)
- 3 output formats: text, JSON, markdown
- CI-friendly exit codes (0/1/2)
- Transitive dependency scanning (npm)
- Actionable recommendations per violation type

## Tested Against
- OpenClaw npm package (70 deps, correctly classified 48 permissive)
- Multi-ecosystem fixture (npm + pip + go + cargo + gem)
- CI exit codes verified
- Custom policy with exceptions verified
- SPDX parenthesized expressions verified

## Next Steps
- Publish after April 10 (GitHub 14-day wait)

# docker-compose-linter — Status

**Status:** Ready
**Price:** $49
**Created:** 2026-04-09

## Features

- Pure Python 3, no external dependencies (no PyYAML required)
- Custom indentation-based YAML parser handles all docker-compose constructs
- 14 lint rules covering security, best practices, and operational concerns
- Four commands: `lint`, `services`, `ports`, `audit`
- Three output formats: `text` (with color), `json`, `markdown`
- `--strict` mode for CI pipeline integration
- `--ignore` flag to suppress specific rules
- `--min-severity` filter to focus on critical issues
- Port conflict detection across all services
- Hardcoded secret detection (PASSWORD, SECRET, KEY, TOKEN patterns)
- Privileged mode and host-network security warnings
- Resource limits and healthcheck coverage checks

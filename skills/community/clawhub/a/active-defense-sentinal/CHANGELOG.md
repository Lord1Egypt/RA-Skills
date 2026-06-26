# Changelog

## 0.4.0 - 2026-04-21

### Added
- OpenClaw adapter for UI, gateway, session, and context-health checks
- Hermes adapter for profile, tool, cron, and MCP checks
- Host adapter for bounded local defensive telemetry
- Skill scanner adapter for OpenClaw skill-supply-chain scanning
- Explicit scan workflow and quarantine policy docs
- Executable helper scripts for local scanning, staged installs, quarantine, and adapter health checks
- Publication-ready README and clawhub.ai listing copy

### Safety notes
- Read-only by default
- High/Critical skill-scan findings are blocked by default
- Quarantine is limited to already-installed skills in the active OpenClaw skill tree
- No stealth, persistence, or destructive auto-remediation

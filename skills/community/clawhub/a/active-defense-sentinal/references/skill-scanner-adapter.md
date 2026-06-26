# Skill Scanner Adapter

This adapter covers the OpenClaw skill supply chain.

## Scope
- Scan candidate skills before installation
- Scan installed skills on change
- Flag risky skill content before activation
- Quarantine high-risk skills when policy allows

## Proven workflow
The scanner behavior is modeled after the `openclaw-skill-scanner` repo and the `cisco-ai-defense/skill-scanner` engine.

### Manual folder scan
```bash
uv run skill-scanner scan /path/to/skill --format markdown --detailed --output /tmp/skill-report.md
```
Use this before copying a local skill into the active skill tree.

### Bulk scan of a directory
```bash
uv run skill-scanner scan-all ~/.openclaw/skills --format markdown --detailed --output /tmp/skills-report.md
```
Use this for scans of the active skill tree or bundled skill collections.

### ClawHub staged install
```bash
npx -y clawhub --workdir "$STAGE_DIR" --dir skills install <slug> [--version <version>]
```
Scan the staged copy before installation.

## Severity policy
- High/Critical: block or quarantine
- Medium/Low/Info: allow with warning summary
- Unknown or unreadable report: review manually

## Evidence to collect
- Source repo or slug
- Scan report path
- Findings by severity
- Install or quarantine action taken
- Timestamp and target path

## Safe default
- Prefer read-only scanning
- Only perform quarantine when explicitly enabled by policy
- Never silently install a skill that has not been scanned

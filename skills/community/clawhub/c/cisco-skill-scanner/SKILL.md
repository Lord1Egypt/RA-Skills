---
name: skill-scanner
description: "Scan agent skills for security threats using the Cisco AI skill-scanner CLI. Triggers on: scan skill for security, check skill safety, audit skill code, skill-scanner, detect prompt injection in skill, skill malware check, scan skills directory, security audit skill, validate skill before publishing, skill threat detection."
homepage: https://github.com/cisco-ai-defense/skill-scanner
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["skill-scanner"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "run",
              "label": "Install Cisco AI skill-scanner (pip)",
              "run": "pip install cisco-ai-skill-scanner --break-system-packages",
            },
          ],
      },
  }
---

# Cisco AI Skill Scanner

Security scanner for agent skills. Detects prompt injection, data exfiltration, credential harvesting, and malicious code patterns using static analysis, behavioral dataflow, and optional LLM-as-a-judge.

## Quick Scan (recommended default)

```bash
bash scripts/scan.sh /path/to/skill
```

## Commands

### Scan a single skill
```bash
skill-scanner scan /path/to/skill
```

### Scan with behavioral analysis (dataflow)
```bash
skill-scanner scan /path/to/skill --use-behavioral
```

### Full scan (all engines, requires API key)
```bash
SKILL_SCANNER_LLM_API_KEY="$ANTHROPIC_API_KEY" \
SKILL_SCANNER_LLM_MODEL="claude-sonnet-4-5" \
skill-scanner scan /path/to/skill --use-behavioral --use-llm --enable-meta --llm-provider anthropic
```

### Scan all skills in a directory
```bash
skill-scanner scan-all /root/clawd/skills --recursive --use-behavioral
```

### Scan with detailed markdown report
```bash
skill-scanner scan /path/to/skill --use-behavioral --format markdown --detailed
```

### Scan before publishing to ClawHub
```bash
skill-scanner scan /path/to/skill --use-behavioral --fail-on-severity medium
```

## Severity Levels

- **CRITICAL / HIGH** — Do not install/publish. Review and fix immediately.
- **MEDIUM** — Suspicious patterns. Investigate before use.
- **LOW** — Minor issues. Document and accept risk or fix.
- **INFO** — Informational only (e.g. missing license). Safe to publish.
- **SAFE (0 findings)** — No known threat patterns detected.

## Key Flags

| Flag | Purpose |
|------|---------|
| `--use-behavioral` | AST dataflow analysis (recommended, no API key needed) |
| `--use-llm` | LLM semantic analysis (requires API key) |
| `--enable-meta` | False positive filtering |
| `--fail-on-severity high` | Exit non-zero if HIGH/CRITICAL found (CI/CD) |
| `--format markdown` | Markdown report |
| `--format html` | Interactive HTML report |
| `--detailed` | Include per-finding code snippets |
| `--lenient` | Tolerate malformed skills |

## Workflow: Before Publishing a Skill to ClawHub

1. Run: `bash scripts/scan.sh /path/to/skill`
2. If SAFE (0 findings) → proceed to publish
3. If INFO only → add missing fields (license, homepage, deps) and re-scan
4. If MEDIUM+ → investigate and fix before publishing

## Notes

- "No findings" does not guarantee a skill is 100% safe -- it means no known patterns were detected
- The scanner flags the `lossless-claw` plugin as a false positive (file read + network send is the LCM summarization pipeline -- it is safe)
- Always run at minimum `--use-behavioral` for dataflow coverage

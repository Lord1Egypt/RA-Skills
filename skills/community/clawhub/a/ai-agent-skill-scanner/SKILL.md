---
name: AI Agent Skill Scanner
version: 2.1.0
description: "Security scanner for AI agent skills. Detects hardcoded secrets, unsafe code execution, prompt injection, and malware patterns in under 50ms. Scan before you install."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔒",
        "tags": ["security", "scanner", "malware-detection", "prompt-injection", "secrets-detection", "code-scanning", "skill-safety"],
      },
  }
---

# AI Agent Skill Scanner 🔒

**Scan any skill for security issues before you install it.** Detects hardcoded secrets, unsafe code execution, prompt injection, and malware patterns in under 50ms.

## How to Use

```bash
# Scan any installed skill folder
python3 scripts/vetter.py /path/to/skill

# JSON output for scripting
python3 scripts/vetter.py /path/to/skill --json
```

## What It Detects

| Issue | Severity | Example |
|-------|----------|---------|
| `eval()` / `exec()` | Critical | Runs arbitrary code |
| Pipe to shell | Critical | `curl ... | bash` |
| Destructive commands | Critical | `rm -rf /`, `mkfs.` |
| `os.system()` | Critical | Shell commands |
| Hardcoded API keys | High | `api_key`, `apikey` |
| `shell=True` | High | Shell injection risk |
| Hardcoded secrets | High | `auth_token`, `secret` |
| Credential file access | High | `.ssh/`, `.aws/` |
| Sudo elevation | High | `sudo` commands |
| Base64 obfuscation | High | Hidden code execution |
| Git config access | High | `.git/config` reads |
| Password hardcoding | High | `password` literal |
| Permission overrides | Medium | `chmod 777` |
| Network calls | Medium | `requests.post()` |

## New in v2.1

- 10 new detection signatures (pipe-to-shell, sudo escalation, destructive commands, credential file access, base64 obfuscation, git config, permission overrides)
- Skips `node_modules/`, `__pycache__/`, `.git/` (reduced false positives)
- Smarter pipe-to-shell detection (only flags actual pipe patterns)
- Self-scan exclusions (scanner ignores its own signatures file)
- `--verbose` flag for skipped file counts

## Example Result

```
Scanned 430 files in 368ms (skipped 6)
Found 1 issue(s):
  [CRITICAL] pipe-to-shell at install.sh:26
    → Remote code execution risk: downloading and piping to shell
```

## Install

```bash
clawhub install ai-agent-skill-scanner
```

## Notes

- Text matching — won't catch obfuscated code
- Always scan skills from unknown publishers before installing
- Quick scan prevents accidents (50ms per skill)

## Feedback

`clawhub star ai-agent-skill-scanner` — `clawhub sync`
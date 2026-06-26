# skill-audit

Newly installed OpenClaw skill safety inspector & audit tool.

## Purpose

Automatically audit newly installed skills before activation. Validates structure, security, and basic health to prevent broken or malicious skills from affecting the system.

## When to Use

- After installing a new skill from ClawHub
- Before enabling a skill for the first time
- When debugging a malfunctioning skill
- As part of routine skill maintenance

## What It Checks

### 1. Structure Validation
- `SKILL.md` exists and is readable
- Required fields present: `name`, `description`, `location`
- No broken internal links or references

### 2. Security Scan
- No hardcoded secrets, API keys, or credentials
- No suspicious external network calls (untrusted URLs)
- File permissions safe (no world-writable scripts)

### 3. Health Check
- Skill directory accessible
- No circular imports or broken references
- Basic syntax validity of SKILL.md

## Usage

```
skill-audit <skill-path>
```

Example:
```
skill-audit ~/.openclaw/skills/my-new-skill
skill-audit /workspace/skills/awesome-skill
```

## Output

- PASS  -- Skill passes all checks
- WARN  -- Minor issues found (non-blocking)
- FAIL  -- Critical issues found (blocking)
- INFO  -- Informational notes

## Notes

- Run as part of your installation workflow, not just when things break
- Combine with clawhub skill for full install -> audit -> enable flow

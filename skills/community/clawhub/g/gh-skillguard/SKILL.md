---
name: gh-skillguard
description: "Run a complete security audit on any OpenClaw SKILL.md in one call. Combines malware scanning (SkillScan), permission scope analysis (ScopeCheck), and prompt injection detection (PromptGuard) into a single unified report with a SAFE/CAUTION/DANGEROUS verdict."
metadata: {"openclaw":{"emoji":"🏰","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","pyyaml"]}]}}
---

# SkillGuard

Full security audit of a SKILL.md — three checks, one call.

## Start the server

```bash
uvicorn skillguard.app:app --port 8005
```

## Audit a skill

```bash
curl -s -X POST http://localhost:8005/v1/audit-skill \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat path/to/SKILL.md | jq -Rs)}" | jq
```

Returns `verdict` (SAFE/CAUTION/DANGEROUS), `total_findings`, and three sub-reports:

- **scan** — malware detection (safety_score, findings, verdict)
- **scope** — permission analysis (declared vs detected, undeclared_access)
- **injection** — prompt injection (risk_score, patterns_detected)

## Why use SkillGuard instead of individual tools?

One call instead of three. Same price. Combined verdict logic: if the malware scan finds anything, it's DANGEROUS. If only scope or injection issues, it's CAUTION. Clean skill = SAFE.

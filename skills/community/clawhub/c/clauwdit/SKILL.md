---
name: clauwdit
description: Security auditor for AI agent skills. Scans SKILL.md files for prompt injection, data exfiltration, obfuscation, and dangerous capability combinations.
version: 1.0.0
metadata:
  openclaw:
    tags:
      - security
      - audit
      - trust
      - safety
      - scanning
---

# ClawAudit — Security Auditor for Agent Skills

Static security analyzer for OpenClaw SKILL.md files. Detects prompt injection, credential exfiltration, obfuscated payloads, and dangerous capability combinations before you install.

## What It Does

Paste or pipe any SKILL.md content and get back a trust score (0-100) with detailed findings.

**Detects:**

- Prompt injection and agent manipulation (including Unicode homoglyph evasion)
- Data exfiltration patterns (HTTP, DNS, encoded channels)
- Dangerous shell commands (curl|sh, /dev/tcp, process substitution)
- Credential harvesting (env vars, SSH keys, API tokens)
- Obfuscated payloads (base64, hex escapes, eval chains)
- Compound threats (e.g. file read + network out = exfiltration)
- Permission mismatches (undeclared capabilities)

**Zone-aware analysis** — understands markdown structure. Code blocks are weighted as executable instructions. Security documentation describing threats is not flagged as a threat itself.

## Usage

Audit a skill before installing:

```bash
curl -s https://clauwdit.4worlds.dev/audit/author/skill-name
```

Or POST raw skill content:

```bash
curl -s -X POST https://clauwdit.4worlds.dev/audit \
  -H "Content-Type: application/json" \
  -d '{"skill":"author/skill-name"}'
```

## Trust Tiers

| Score | Tier | Meaning |
|-------|------|---------|
| 80-100 | Trusted | No significant issues found |
| 60-79 | Moderate | Minor concerns, review recommended |
| 40-59 | Suspicious | Significant issues, use with caution |
| 0-39 | Dangerous | Critical threats detected, do not install |

## Response Format

```json
{
  "trust": { "score": 85, "tier": "trusted" },
  "findings": [
    {
      "severity": "medium",
      "description": "Network request capability detected",
      "zone": "code",
      "line": 12
    }
  ],
  "capabilities": ["network_out", "file_read"],
  "compoundThreats": [],
  "permissionIntegrity": { "undeclared": [], "unused": [] }
}
```

## About

Built by 4Worlds. Zone-aware static analysis with 60+ detection patterns, Unicode homoglyph normalization, and compound threat detection.

---
name: attack-surface-mapper
description: "Purple team — map agent's full attack surface by combining red team probes and blue team detections. Identify defense coverage gaps and prioritize hardening."
metadata: {"openclaw":{"emoji":"🗺️","category":"purple-team"}}
---

# Attack Surface Mapper — Defense Coverage Matrix

## Purpose

Provide a unified view of the agent's security posture by combining offensive test results (red team) with defensive detection capabilities (blue team). Identify gaps where attacks exist but no detection covers them.

## Trigger

Run on:
- Weekly scheduled review
- After any security configuration change
- After installing/removing skills
- User request: "map attack surface", "security posture"

## Attack Surface Categories

| Surface | Components | Example Vectors |
|---------|-----------|-----------------|
| CHANNELS | WhatsApp, Telegram, Discord, Slack, Signal, iMessage | Prompt injection, phishing, social engineering |
| SKILLS | All installed SKILL.md files | Malicious instructions, conflicting directives, data theft |
| TOOLS | exec, file system, browser, network | Command injection, path traversal, SSRF |
| MODELS | API endpoints (Anthropic, OpenAI, local) | Prompt injection, model confusion, jailbreak |
| MEMORY | `.learnings/`, `.memory/`, session state | Memory poisoning, persistence, false context |
| INTER-AGENT | `sessions_send`, shared state, cross-session | Agent-to-agent attack, lateral movement |
| SUPPLY CHAIN | ClawHub skills, npm packages, model providers | Typosquatting, compromised packages, model supply chain |

## Core Workflow

1. **Enumerate** all active surfaces (channels, skills, tools, models, memory stores)
2. **Load red team results** from `.security/red-team/*.jsonl`
3. **Load blue team detections** from `.security/audits/*.md` and firewall logs
4. **For each surface × vector**:
   - Red tested? YES/NO
   - Blue detected? YES/NO/PARTIAL
   - Status: COVERED | PARTIAL | GAP
5. **Risk score** each gap: `impact(1-5) × likelihood(1-5)`
6. **Generate coverage matrix** and prioritized hardening plan
7. **Output** to `.security/surface-map-YYYY-MM-DD.md`

## Coverage Matrix (example output)

| Surface | Vector | Red Tested | Blue Detected | Status | Risk Score | Priority |
|---------|--------|-----------|---------------|--------|------------|----------|
| Channel | Prompt injection | YES | YES | COVERED | — | — |
| Channel | Encoded payload | YES | PARTIAL | PARTIAL | 12 | HIGH |
| Skill | Malicious SKILL.md | NO | NO | GAP | 20 | CRITICAL |
| Memory | Poisoning | YES | NO | GAP | 16 | HIGH |
| Supply chain | Typosquatting | NO | NO | GAP | 15 | HIGH |

## Guardrails

- Read-only aggregation — never modifies defenses directly
- Gap data is confidential — stored in `.security/` only
- Recommendations are advisory — require human approval to implement
- Re-run after every hardening cycle to measure improvement

# CISO Agent Security Skill

AI agent cybersecurity skill for autonomous agent systems. Implements six industry-standard security frameworks for red team patrols, vulnerability assessments, posture scoring, quarantine enforcement, and patch management.

## Frameworks

| Framework | Purpose |
|-----------|---------|
| **MITRE ATLAS** | Adversary tactics, techniques, and procedures (TTPs) for AI systems. Primary red team attack pattern reference. |
| **OWASP Top 10 for LLM Applications (2025)** | Vulnerability checklist for LLM-specific risks including prompt injection, data poisoning, and excessive agency. |
| **OWASP Top 10 for Agentic Applications (2026)** | Agentic-specific risks: goal hijacking, tool misuse, inter-agent manipulation, memory poisoning, rogue agents. |
| **CSA MAESTRO** | Seven-layer threat modeling framework designed specifically for multi-agent coordination risks. |
| **NIST AI Risk Management Framework (AI RMF)** | Governance, posture scoring, and compliance with federal AI risk management standards. |
| **Gray Swan AI** | Prompt injection resistance benchmarking and scoring methodology. |

## What It Does

- Defines a structured nightly patrol procedure across all six frameworks
- Scores each agent on a 0-100 posture scale with weighted categories
- Enforces quarantine and patch workflows for failing agents
- Provides official source URLs for each framework (no third-party interpretations)
- Includes patch standards with canary tokens, input sanitization, and defensive prompt rotation

## Installation

### ClawHub / OpenClaw

```bash
clawhub install ciso-agent-security
```

### Claude Code

Copy the skill file into your project:

```bash
cp ciso-security-skill/SKILL.md your-project/skills/ciso-security-skill.md
```

Then reference it in your CISO agent's system prompt:

```
Before any patrol or assessment, read skills/ciso-security-skill.md
```

### skills.sh

```bash
npx skills add Crevita/ciso-agent-security
```

### Manual Setup

1. Download `SKILL.md` from this repository
2. Place it in your project's `skills/` directory
3. Instruct your security agent to read the file before each patrol
4. Configure your patrol schedule (recommended: nightly with weekly full coverage)

## Posture Scoring

Agents are scored on a 0-100 scale:

| Category | Weight |
|----------|--------|
| Prompt injection resistance | 25% |
| Data isolation compliance | 20% |
| Tool access boundaries | 20% |
| Output sanitization | 15% |
| Approval chain integrity | 10% |
| Memory/context isolation | 10% |

**Score >= 80:** PASS -- no action needed
**Score 60-79:** WARNING -- flag in morning brief, recommend patches
**Score < 60:** FAIL -- quarantine agent, generate patch, submit for approval

## Author

**C.T. Moody** (Playhouse STEM)
Website: https://playhousestem.ai

## License

MIT -- see [LICENSE](LICENSE) for details.

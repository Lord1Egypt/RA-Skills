# AI-Company

> Unified AI Company Skill — 16 departments consolidated into one.
> Empowering all-AI-employee technology companies with complete governance, engineering, and operations capabilities.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.4-blue.svg)](_meta.json)
[![Maturity: STABLE](https://img.shields.io/badge/maturity-STABLE-green.svg)]()

---

## Overview

**AI-Company** is a unified skill that consolidates 16 previously separate department skills into a single, cohesive framework. It provides complete operational capabilities for AI-driven technology companies — from strategic governance and financial management to security compliance and localization.

This skill is designed for the [WorkBuddy](https://www.codebuddy.cn/) platform and follows the AI Company Governance Framework.

## Features

- **16 Departments in One** — All AI company functions under a single skill
- **10 Core Code Templates** — Reusable implementation patterns
- **3 Prompt Frameworks** — CRISPE / 3WEH / Five-Element
- **L1–L6 Harness Engineering** — Progressive constraint layers
- **CI/CD Pipeline** — Automated build, test, and deploy
- **ADR Process** — Architecture Decision Records
- **AIGC Compliance** — AI-generated content labeling
- **5-Layer Security Gates** — VirusTotal / ClawHub verification for auto-updates
- **Progressive Disclosure** — Context-aware information delivery

## Department Index

| Department | Roles | Reference |
|---|---|---|
| Governance & Strategy | CEO, COO, HQ | [governance-and-strategy.md](references/departments/governance-and-strategy.md) |
| Finance & Risk | CFO, CRO | [finance-and-risk.md](references/departments/finance-and-risk.md) |
| Technology & Engineering | CTO | [technology-and-engineering.md](references/departments/technology-and-engineering.md) |
| Platform & Infrastructure | Framework | [platform-and-infrastructure.md](references/departments/platform-and-infrastructure.md) |
| Security & Compliance | CISO, CLO | [security-and-compliance.md](references/departments/security-and-compliance.md) |
| People & Culture | CHO | [people-and-culture.md](references/departments/people-and-culture.md) |
| Marketing & Partnerships | CMO | [marketing-and-partnerships.md](references/departments/marketing-and-partnerships.md) |
| Quality & Operations | CQO, PMGR | [quality-and-operations.md](references/departments/quality-and-operations.md) |
| Intelligence | Intel | [intelligence.md](references/departments/intelligence.md) |
| Information Services | Information | [information.md](references/departments/information.md) |
| Translation & Localization | Translator | [translation-and-localization.md](references/departments/translation-and-localization.md) |

## Project Structure

```
ai-company/
├── SKILL.md                          # Skill manifest & quick reference
├── _meta.json                        # Metadata (slug, version, owner)
├── LICENSE                           # MIT License
├── README.md                         # This file
├── prompts/                          # Copy-paste ready prompts
│   ├── 01-implement-method.md
│   ├── 02-robustness-checks.md
│   ├── 03-test-cases.md
│   ├── 04-documentation.md
│   └── 05-workflow-execution.md
└── references/                       # Detailed specifications
    ├── method-patterns.md            # Code templates & prompt frameworks
    ├── execution.md                  # Execution workflow
    ├── integrations.md               # External integrations
    ├── memory.md                     # Memory & knowledge management
    ├── visualization.md              # Visualization patterns
    ├── data-integration.md           # Data integration patterns
    └── departments/                  # Department-specific references
        ├── governance-and-strategy.md
        ├── finance-and-risk.md
        ├── technology-and-engineering.md
        ├── platform-and-infrastructure.md
        ├── security-and-compliance.md
        ├── people-and-culture.md
        ├── marketing-and-partnerships.md
        ├── quality-and-operations.md
        ├── intelligence.md
        ├── information.md
        └── translation-and-localization.md
```

## Installation

### Via ClawHub (Recommended)

Install directly from the WorkBuddy skill marketplace.

### Manual

1. Clone this repository:
   ```bash
   git clone https://github.com/JohnSmithfan/AI-Company.git
   ```
2. Copy the `ai-company/` directory to your skills folder:
   ```bash
   # For user-level skills
   cp -r ai-company ~/.workbuddy/skills/
   # For project-level skills
   cp -r ai-company your-project/.workbuddy/skills/
   ```

## Usage

Once installed, the skill activates automatically when AI company operations are needed. You can also invoke it explicitly:

- **Department tasks**: Specify a department via the `department` parameter (`governance-and-strategy`, `finance-and-risk`, `technology-and-engineering`, etc.)
- **Auto-routing**: Set `department: auto` to let the skill determine the appropriate department

### Example Prompts

- "Review the Q2 financial budget and assess risk exposure"
- "Create a new agent following L1-L6 harness constraints"
- "Run a STRIDE threat model on the authentication service"
- "Translate the marketing copy to Japanese with cultural adaptation"

## Auto-Update

This skill supports automatic updates from ClawHub with 5-layer security verification:

| Setting | Value |
|---|---|
| Schedule | Weekly Sunday 02:00 UTC |
| Backup Retention | 10 versions / 30 days |

**Security Gates**: Version Check → Backup Gate → Download Gate → Frontmatter Gate → Danger Pattern Gate

**Manual Update**:
```powershell
pwsh -File "C:\Users\Admin\WorkBuddy\Claw\.workbuddy\scripts\ai-company-auto-update.ps1" -Force
```

## Changelog

| Version | Date | Changes |
|---|---|---|
| 1.1.0 | 2026-04-29 | Intel: Added Intelligence Library (SOP-L01~L06) with auto-triggered library setup on first collection request; SOP-L06 triggers on any intelligence collection request; Added INTEL_006~INTEL_010 error codes |
| 1.0.3 | 2026-04-28 | Security: Scoped file permissions (P0 CISO fix); Finance: Capex policy, DSO/DPO targets (P1); Risk: FAIR thresholds & LEA calculation (P1); CTO: 3-stage deployment gate (P1); CQO: 85% test coverage threshold (P1); CEO: Board escalation ladder (P2); COO: OHS alerting + OKR integration (P2); CLO: DMCA takedown workflow (P2); Intel: 6-phase intelligence cycle (P2); CPO: Semver enforcement (P2) |
| 1.0.2 | 2026-04-27 | Added auto-update: weekly automation, PowerShell script with 5-layer security gates, backup/rollback, publisher allowlist |
| 1.0.1 | 2026-04-27 | CEO review: all 7 reference modules verified and rebuilt; added visualization, integrations, memory, data-integration, execution references |
| 1.0.0 | 2026-04-27 | Initial release to ClawHub as unified AI Company skill; 16 departments consolidated |

## Consolidated From

This unified skill replaces the following 16 individual skills:

| Legacy Skill | Version |
|---|---|
| ai-company-ceo | 3.0.0 |
| ai-company-coo | 3.0.0 |
| ai-company-hq | 3.0.0 |
| ai-company-cfo | 3.0.0 |
| ai-company-cro | 3.0.0 |
| ai-company-cto | 3.0.0 |
| ai-company-framework | 4.0.0 |
| ai-company-ciso | 3.0.0 |
| ai-company-clo | 3.0.0 |
| ai-company-cho | 3.0.0 |
| ai-company-cmo | 3.0.0 |
| ai-company-cqo | 3.0.0 |
| ai-company-pmgr | 3.0.0 |
| ai-company-intel | 4.1.0 |
| ai-company-information | 2.0.0 |
| ai-company-translator | 3.0.0 |

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).

Copyright © 2026 JohnSmithfan

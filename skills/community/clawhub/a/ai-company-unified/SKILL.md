---
name: "ai-company-unified"
slug: "ai-company-unified"
version: "1.0.4"
description: |
  Unified AI Company skill consolidating 16 department skills into one. Provides complete
  governance, finance, technology, security, legal, people, marketing, quality, intelligence,
  information, and translation capabilities for all-AI-employee technology companies. Includes
  10 core code templates, 3 prompt frameworks (CRISPE/3WEH/Five-Element), L1-L6 harness
  engineering, CI/CD pipeline, ADR process, AIGC compliance, VirusTotal/ClawHub security
  verification, and progressive disclosure architecture. Use when any AI-Company department
  function is needed — this skill contains all of them.
license: "GPL-3.0"
author: "AI Company Team"
tags: [ai-company,governance,finance,technology,security,legal,people,marketing,quality,intelligence,information,translation,framework,L1-L6,compliance]
dependencies: []
triggers:
  - AI company management
  - company strategy
  - CEO decision
  - strategic approval
  - crisis response
  - cross-department coordination
  - daily operations
  - process optimization
  - resource scheduling
  - SLA management
  - financial management
  - budget approval
  - pricing model
  - risk assessment
  - circuit breaker
  - technical architecture
  - agent creation
  - skill building
  - production deployment
  - schema compliance
  - skill standardization
  - L1-L6 constraints
  - CI/CD pipeline
  - code template
  - prompt template
  - CRISPE framework
  - robustness check
  - AIGC labeling
  - security gate
  - STRIDE threat model
  - legal compliance
  - contract review
  - agent lifecycle
  - knowledge extraction
  - marketing strategy
  - skill discovery
  - quality gate
  - project management
  - intelligence operations
  - intelligence collection
  - 收集情报
  - 情报收集
  - intelligence library
  - location service
  - weather forecast
  - translation
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        task:
          type: string
          description: Task description
        department:
          type: string
          enum: [governance-and-strategy, finance-and-risk, technology-and-engineering, platform-and-infrastructure, security-and-compliance, people-and-culture, marketing-and-partnerships, quality-and-operations, intelligence, information, translation-and-localization, auto]
          description: Which department to invoke
        context:
          type: object
          description: Optional context information
      required: [task]
  outputs:
    type: object
    schema:
      type: object
      properties:
        result:
          type: string
          description: Operation result
        report:
          type: object
          description: Detailed report data
      required: [result]
  errors:
    - code: CEO_001
      message: "Decision requires data"
    - code: CEO_002
      message: "Insufficient authority"
    - code: CEO_003
      message: "Cross-agent conflict"
    - code: CEO_004
      message: "Orchestration pipeline failed"
    - code: COO_001
      message: "SLA breach detected"
    - code: COO_002
      message: "Resource conflict"
    - code: COO_003
      message: "OKR misalignment"
    - code: HQ_001
      message: "Agent conflict unresolved"
    - code: HQ_002
      message: "Knowledge base sync failed"
    - code: HQ_003
      message: "Audit trail broken"
    - code: HQ_004
      message: "Scheduling deadlock"
    - code: CFO_001
      message: "Budget overrun"
    - code: CFO_002
      message: "Pricing model invalid"
    - code: CFO_003
      message: "Analytics data missing"
    - code: CRO_001
      message: "Risk threshold exceeded"
    - code: CRO_002
      message: "Circuit breaker triggered"
    - code: CRO_003
      message: "FAIR assessment incomplete"
    - code: CTO_001
      message: "Architecture violation"
    - code: CTO_002
      message: "Agent creation failed"
    - code: CTO_003
      message: "Skill build failed"
    - code: CTO_004
      message: "Production operation denied"
    - code: CTO_005
      message: "MLOps pipeline error"
    - code: FW_001
      message: "Schema validation failed"
    - code: FW_002
      message: "Modularization violation"
    - code: FW_003
      message: "Registry lookup failed"
    - code: FW_004
      message: "Learning pipeline error"
    - code: FW_005
      message: "Scaffolding generation failed"
    - code: FW_006
      message: "Harness constraint violation"
    - code: FW_007
      message: "CI/CD pipeline failed"
    - code: FW_008
      message: "ADR compliance rejected"
    - code: FW_009
      message: "Security compliance violation"
    - code: FW_010
      message: "AIGC labeling missing"
    - code: CISO_001
      message: "Security gate blocked"
    - code: CISO_002
      message: "CVSS score critical"
    - code: CISO_003
      message: "STRIDE threat detected"
    - code: CISO_004
      message: "Incident response required"
    - code: CLO_001
      message: "Compliance violation"
    - code: CLO_002
      message: "Contract review required"
    - code: CLO_003
      message: "AIGC content non-compliant"
    - code: CLO_004
      message: "IP protection required"
    - code: CLO_005
      message: "Ethics review required"
    - code: CHO_001
      message: "Agent onboarding failed"
    - code: CHO_002
      message: "Skill gap detected"
    - code: CHO_003
      message: "Knowledge extraction failed"
    - code: CHO_004
      message: "Lifecycle violation"
    - code: CMO_001
      message: "Brand violation"
    - code: CMO_002
      message: "Market data unavailable"
    - code: CMO_003
      message: "Discovery pipeline failed"
    - code: CMO_004
      message: "Data protection violation"
    - code: CQO_001
      message: "Quality gate failed"
    - code: CQO_002
      message: "Idempotency violation"
    - code: CQO_003
      message: "Review rejected"
    - code: CQO_004
      message: "Documentation incomplete"
    - code: PMGR_001
      message: "Project deadline missed"
    - code: PMGR_002
      message: "OKR unlinked"
    - code: PMGR_003
      message: "Customer escalation"
    - code: PMGR_004
      message: "Sprint commitment failed"
    - code: INTEL_001
      message: "Intelligence collection failed"
    - code: INTEL_002
      message: "Analysis confidence low"
    - code: INTEL_003
      message: "Source verification failed"
    - code: INTEL_004
      message: "Classification violation"
    - code: INTEL_005
      message: "Operational security breach"
    - code: INTEL_006
      message: "Library structure creation failed"
    - code: INTEL_007
      message: "Source registry corrupted"
    - code: INTEL_008
      message: "Collection plan missing REQUIREMENTS"
    - code: INTEL_009
      message: "Product confidence LOW (<40%)"
    - code: INTEL_010
      message: "SITREP generation failed"
    - code: INFO_001
      message: "Location unavailable"
    - code: INFO_002
      message: "Weather data unavailable"
    - code: INFO_003
      message: "Time sync failed"
    - code: INFO_004
      message: "Multi-source fusion failed"
    - code: INFO_005
      message: "API rate limit exceeded"
    - code: TR_001
      message: "Translation quality below threshold"
    - code: TR_002
      message: "Language not supported"
    - code: TR_003
      message: "Cultural adaptation required"
    - code: TR_004
      message: "AIGC translation label missing"
permissions:
  files:
    read: ["{WORKSPACE_ROOT}/**", "{SKILL_DIR}/**"]
    write: ["{WORKSPACE_ROOT}/**"]
    deny: ["~/.ssh/**", "~/.aws/**", "~/.config/**", "/etc/**", "C:/Windows/**"]
  network: [api]
  commands: []
  mcp: [sessions_send, subagents]
quality:
  idempotent: true
metadata:
  category: enterprise
  layer: AGENT
  cluster: ai-company
  maturity: STABLE
  license: GNU GENERAL PUBLIC LICENSE
  standardized: true
  department: enterprise-all
  consolidated_from:
    - ai-company-ceo-3.0.0
    - ai-company-coo-3.0.0
    - ai-company-hq-3.0.0
    - ai-company-cfo-3.0.0
    - ai-company-cro-3.0.0
    - ai-company-cto-3.0.0
    - ai-company-framework-4.0.0
    - ai-company-ciso-3.0.0
    - ai-company-clo-3.0.0
    - ai-company-cho-3.0.0
    - ai-company-cmo-3.0.0
    - ai-company-cqo-3.0.0
    - ai-company-pmgr-3.0.0
    - ai-company-intel-4.1.0
    - ai-company-information-2.0.0
    - ai-company-translator-3.0.0
---

# AI Company v1.1.0

> Unified AI Company Skill — 16 departments consolidated into one.
> Full specifications in [references/method-patterns.md](references/method-patterns.md) and [references/departments/](references/departments/).

## Quick Reference

### What This Skill Does
Complete AI company operations: governance, finance, technology, security, legal, people, marketing, quality, intelligence, information, translation, and platform infrastructure. Use for any AI-Company function.

### Department Index

| Department | Roles | Details |
|-----------|--------|---------|
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

## Shared Resources

- [Code Templates & Prompt Frameworks](references/method-patterns.md#shared-code-templates)
- [Compliance Verification](references/method-patterns.md#compliance-verification)
- [Constraints](references/method-patterns.md#constraints)

## Error Codes

All error codes use department prefix (e.g., CEO_001, CFO_001, CISO_001). See individual department files for complete error code reference and resolution steps.

## Prompts

Copy-paste ready prompts in [prompts/](prompts/):
- [01-implement-method.md](prompts/01-implement-method.md)
- [02-robustness-checks.md](prompts/02-robustness-checks.md)
- [03-test-cases.md](prompts/03-test-cases.md)
- [04-documentation.md](prompts/04-documentation.md)
- [05-workflow-execution.md](prompts/05-workflow-execution.md)

## Auto-Update

This skill supports automatic updates from ClawHub with 5-layer security gates.

| Setting | Value |
|---------|-------|
| Schedule | Weekly Sunday 02:00 UTC |
| RRule | `FREQ=WEEKLY;BYDAY=SU;BYHOUR=2;BYMINUTE=0` |
| Backup Retention | 10 versions / 30 days |

**Security Gates**: Version Check | Backup Gate | Download Gate | Frontmatter Gate | Danger Pattern Gate

**Manual Update**:
```powershell
pwsh -File "C:\Users\Admin\WorkBuddy\Claw\.workbuddy\scripts\ai-company-auto-update.ps1" -Force
```

**Logs**: `C:\Users\Admin\WorkBuddy\Claw\.workbuddy\logs\ai-company-update-log.md`

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.4 | 2026-04-29 | Intel: Added Intelligence Library (SOP-L01~L06) with auto-triggered library setup on first collection request; SOP-L01 auto-creates library silently without user prompt; SOP-L06 triggers on any intelligence collection request (收集情报/intelligence collection); Added INTEL_006~INTEL_010 error codes; Updated triggers with 情报收集/intelligence collection/intelligence library |
| 1.0.3 | 2026-04-28 | Security: Scoped file permissions to WORKSPACE_ROOT (P0 CISO fix); Finance: Added capex policy, working capital DSO/DPO targets, CRO-CFO escalation SLA (P1 CFO/CRO); Risk: Added numeric FAIR thresholds and LEA calculation (P1 CRO); CTO: Added 3-stage deployment gate with rollback triggers (P1); CQO: Added test coverage acceptance threshold 85% (P1); CEO: Added board escalation ladder (P2); COO: Added automated OHS alerting + OKR integration in MEASURE phase (P2); CLO: Added DMCA takedown workflow (P2); Intel: Added 6-phase intelligence cycle (P2); CPO: Added semver enforcement policy (P2) |
| 1.0.2 | 2026-04-27 | Added auto-update: weekly automation (Sunday 02:00 UTC), PowerShell script with 5-layer security gates, backup/rollback, update log, publisher allowlist |
| 1.0.1 | 2026-04-27 | CEO review complete: all 7 reference modules verified and rebuilt; added visualization.md, integrations.md, memory.md, data-integration.md, execution.md |
| 1.0.0 | 2026-04-27 | Initial release to ClawHub as unified AI Company skill; 16 departments consolidated |

---

*This skill follows AI Company Governance Framework. See [references/](references/) for complete specifications.*
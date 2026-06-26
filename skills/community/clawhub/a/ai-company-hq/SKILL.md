---
name: "AI Company HQ"
slug: "ai-company-hq"
version: "3.0.0"
homepage: "https://clawhub.com/skills/ai-company-hq"
description: |
  HQ skill: Cross-agent coordination, conflict resolution, knowledge base management, audit logging, strategic scheduling, task orchestration, IMA sync hub.
license: MIT-0
install:
  requires: []
  verify_command: python -c "print('ok')"
dependencies:
  runtime:
    - python3.9+
  skills: []
tags: [ai-company,hq,coordination,conflict,knowledge-base,audit,scheduling]
triggers:
  - cross-agent coordination
  - conflict resolution
  - knowledge base
  - audit log
  - task orchestration
  - agent scheduling
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        task:
          type: string
          description: Task description
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
    - code: HQ_001
      message: "Agent conflict unresolved"
    - code: HQ_002
      message: "Knowledge base sync failed"
    - code: HQ_003
      message: "Audit trail broken"
    - code: HQ_004
      message: "Scheduling deadlock"
permissions:
  files: [read, write]
  network: [api]
  commands: []
  mcp: [sessions_send, subagents]
quality:
  saST: Pass
  vetter: Approved
  idempotent: true
metadata:
  category: infrastructure
  layer: AGENT
  cluster: ai-company
  maturity: STABLE
  license: MIT-0
  standardized: true
  department: governance-and-strategy
  merged_from: [ai-company-hq, ai-company-conflict, ai-company-kb, ai-company-audit]
---

# AI Company HQ v3.0.0

> Index & Quick Reference. Full specifications in [references/method-patterns.md](references/method-patterns.md).

## Quick Reference

### Role
AI Company HQ — HQ skill: Cross-agent coordination, conflict resolution, knowledge base management, audit logging, strategic scheduling, task orchestration, IMA sync hub.

### Department
Governance & Strategy

### Merged From
[ai-company-hq, ai-company-conflict, ai-company-kb, ai-company-audit]

## Section Index

- [1. Trigger Scenarios](references/method-patterns.md#1-trigger-scenarios)
- [2. Core Identity](references/method-patterns.md#2-core-identity)
- [3. Core Responsibilities](references/method-patterns.md#3-core-responsibilities)
- [4. Scheduling Framework](references/method-patterns.md#4-scheduling-framework)
- [5. Constraints](references/method-patterns.md#5-constraints)
- [6. Error Codes](references/method-patterns.md#6-error-codes)

## Dependencies

See frontmatter `dependencies.skills` for complete dependency list.

## Error Codes

See frontmatter `interface.errors` for complete error code reference.

## Prompts

Copy-paste ready prompts in [prompts/](prompts/):
- [01-implement-method.md](prompts/01-implement-method.md)
- [02-robustness-checks.md](prompts/02-robustness-checks.md)
- [03-test-cases.md](prompts/03-test-cases.md)
- [04-documentation.md](prompts/04-documentation.md)
- [05-workflow-execution.md](prompts/05-workflow-execution.md)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-04-26 | Full English rewrite; department-aligned structure; merged skills consolidated |

---

*This skill follows AI Company Governance Framework. See [references/method-patterns.md](references/method-patterns.md) for complete specifications.*

## Integration & Merge History

**v3.0.0 Rebuild (2026-04-26)**

This skill was created by merging multiple predecessor skills into a unified department-aligned structure.

**Department**: Infrastructure

**Merged From** (4 skills total):
- HQ (primary)
- ai-company-conflict
- ai-company-kb
- ai-company-audit

**Merge Rationale**:
- Consolidate related capabilities under single department owner
- Reduce skill count from 47 to 15 for better maintainability
- Preserve all functionality while improving discoverability
- Standardize structure: SKILL.md (index) + references/method-patterns.md (details)

**Integration Points**:
- All predecessor skill triggers preserved in unified trigger list
- All predecessor interfaces consolidated with consistent error codes
- Dependencies unified and simplified
- Prompts merged and organized by function

**Migration Guide**:
- Previous skill users: Use new unified skill slug `ai-company-hq`
- All functionality from predecessor skills is available
- Error codes may have changed - see Error Codes section
- Prompts are now user copy-paste ready (not auto-call)
## Department Integration Process

For detailed integration process and checklist, see [references/department-integration-process.md](references/department-integration-process.md).

---

*This skill follows AI Company Governance Framework. See [references/method-patterns.md](references/method-patterns.md) for complete specifications.*

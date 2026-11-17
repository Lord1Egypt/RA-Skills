---
name: "ai-company"
slug: "ai-company"
version: "1.0.0"
description: "Micro-tier governance skill for small AI agent organizations (1-3 agents). Consolidates 18 enterprise function blocks into two departments, governance-and-delivery and engineering-and-safety, covering strategy, risk, compliance, architecture, safety, and delivery. Ships ten harness code templates, three prompt frameworks, a full error-code catalog, and a scaling specification. Provides two self-contained human-paste prompts (method implementation, robustness checks) usable in any AI chat window. Source files are authored in English; runtime output follows the user's language per the language policy, with English fallback. Includes propose-only self-scaling that evaluates scaling thresholds and proposes tier upgrades up to group. Use when a small team needs enterprise-grade governance, engineering harnesses, PII masking, AIGC disclosure, or tier-upgrade assessment for its agents."
license: "GPL-3.0"
author: "AI Company Team"
tags: [governance, llm-agents, agent-organization, compliance, error-codes, harness-engineering, pii-masking, aigc-disclosure, self-scaling, micro-tier, method-templates, robustness-checks]
dependencies: []
triggers:
  - evaluate scaling threshold
  - propose tier upgrade
  - review governance policy
  - approve quarterly objectives
  - audit compliance evidence
  - assess organizational risk
  - implement method from specification
  - apply robustness checks to code
  - mask sensitive data in outputs
  - generate trace id for audit trail
  - review error handling design
  - respond in user language
  - translate deliverable content
  - add aigc disclosure to output
  - package deliverable for release
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
          enum: [auto, governance-and-delivery, engineering-and-safety]
          description: Which department to invoke; omit or "auto" to auto-route
        output_language:
          type: string
          description: Override runtime output language; omit to follow the language decision chain
        context:
          type: object
          description: Optional context information
      required: [task]
  outputs:
    type: object
    schema: { type: object, properties: { result: { type: string, description: Operation result }, report: { type: object, description: Detailed report data } }, required: [result] }
errors: []
error_code_prefixes: [CEO_, CTO_, SCL_]
language_policy:
  authoring: en
  encoding: utf-8
  output: user-specified
  fallback: en
  immutable_tokens: [slug, error_code, field_name, enum_value, file_path, function_name]
self_scaling:
  enabled: true
  state_file: .scaling-state.json
  spec: references/scaling.md
  upgrade_policy: propose-only
  max_tier: group
permissions:
  files:
    read:  ["{WORKSPACE_ROOT}/**", "{SKILL_DIR}/**"]
    write: ["{WORKSPACE_ROOT}/**"]
    deny:  ["~/.ssh/**", "~/.aws/**", "~/.config/**", "/etc/**", "{WINDOWS_DIR}/**"]
  network: []
  commands: []
  mcp: [sessions_send, subagents]
quality:
  idempotent: true
metadata:
  category: enterprise
  layer: AGENT
  cluster: governance
  maturity: STABLE
  license: GPL-3.0
  standardized: true
  scale_tier: micro
  department_count: 2
  function_block_count: 18
  harness_baseline: L3
---

# AI Company Governance

Micro-tier (XS) LLM agent governance skill for organizations of 1-3 agents: 18 enterprise function blocks consolidated into 2 departments, backed by shared harness templates, a full error-code catalog, and propose-only self-scaling.

> Source files are authored in English; runtime output follows the user's language (see `language_policy` in the frontmatter). Slugs, error codes, field names, enum values, file paths, and function names are never translated.

## Departments

| Slug | Prefix | Scope | Reference |
|---|---|---|---|
| `governance-and-delivery` | `CEO_` | Strategy, governance, delivery | [governance-and-delivery.md](references/departments/governance-and-delivery.md) |
| `engineering-and-safety` | `CTO_` | Architecture, engineering, safety | [engineering-and-safety.md](references/departments/engineering-and-safety.md) |

## Shared Resources

| Resource | Contents |
|---|---|
| [method-patterns.md](references/method-patterns.md) | Single source of truth for the ten shared code templates and the CRISPE / 3WEH / Five-Element prompt frameworks |
| [error-codes.md](references/error-codes.md) | Full four-element error-code catalog (code, message, trigger, resolution) for all prefixes |
| [scaling.md](references/scaling.md) | Tier thresholds, upgrade gating, and alias mapping for self-scaling |

## Error Code Prefixes

| Prefix | Meaning |
|---|---|
| `CEO_` | Governance-and-delivery department codes |
| `CTO_` | Engineering-and-safety department codes |
| `SCL_` | Self-scaling infrastructure codes (fixed across tiers) |

## Prompts

| File | Mode | Purpose |
|---|---|---|
| [01-implement-method.md](prompts/01-implement-method.md) | `human-paste` | Paste into any AI chat window to have that AI implement one method to this standard |
| [02-robustness-checks.md](prompts/02-robustness-checks.md) | `human-paste` | Paste into any AI chat window to have that AI run robustness checks on a method |

## Quick Start

1. Invoke the skill with `task` (required) and optionally `department` (`auto` routes automatically); set `output_language` to override the runtime output language.
2. For implementation standards, use the shared templates in [method-patterns.md](references/method-patterns.md); for failures, look up codes by prefix in [error-codes.md](references/error-codes.md).
3. To work outside this skill, open [01-implement-method.md](prompts/01-implement-method.md) or [02-robustness-checks.md](prompts/02-robustness-checks.md), fill in the `<placeholders>`, and paste the prompt into any AI chat window.
4. When the organization grows, ask the skill to evaluate scaling thresholds or propose a tier upgrade; the rules live in [scaling.md](references/scaling.md).

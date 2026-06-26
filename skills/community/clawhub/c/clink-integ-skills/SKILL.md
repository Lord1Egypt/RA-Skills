---
name: clink-integ-skills
description: Design, scaffold, validate, and review Clink standard integrations, new user onboarding, merchant skill for generic agent integrations, merchant skill for OpenClaw integrations, and documentation-backed contracts.
---

# clink-integ-skills

Use this skill when the user wants to guide a coding agent through a Clink integration, validate the integration approach, review an existing design, or answer a documentation-backed integration question.

This skill is modular:

- do not invent endpoints, fields, events, or product behavior
- keep the main skill file short and push detailed process into modules
- prefer output artifacts that developers can execute or review directly
- guide implementation decisions without pretending to generate final project-specific integration code blindly

## Scope

This skill covers four primary guidance paths:

- standard integration, including checkout session creation, webhook contract review, and optional embedded form integration through JS SDK
- new user onboarding, including docs-backed first-time dashboard, account, API key, product, webhook, and first checkout setup guidance
- merchant skill for generic agent integration, including non-OpenClaw agent runtime contracts through `agentic-payment-skills`, adapter design, `clink-cli` payment execution, callback, and task resume behavior
- merchant skill for OpenClaw integration, including OpenClaw merchant skill integration through `openclaw-payment-skills` and merchant backend webhook support for email verification

It also provides support capabilities for:

- Clink documentation-backed guidance, including explaining official docs, answering doc-based integration questions, and extracting the relevant contract details from official docs
- integration validation, including handoff contract validation, webhook-design validation, and integration guidance artifacts

## Routing

### New User Onboarding

Use this path when the user wants help with:

- new user onboarding
- getting started, quickstart, first-time setup, or first checkout
- initial dashboard setup before integration
- account invitation, password setup, MFA setup, merchant selection, or user access
- initial Secret Key, product, webhook, and first checkout preparation

Read:

- `references/retrieval-protocol.md`
- run `node scripts/load_official_docs.mjs`
- `references/new-user-onboarding.md`

After drafting the solution, review it with:

- `references/review-checklist.md`
- `references/output-artifacts.md`

### Standard Integration

Use this path when the user wants help with:

- hosted checkout
- checkout session creation
- merchant backend implementation
- webhook registration and verification
- optional embedded form integration through JS SDK
- configured link opening flow
- order and refund synchronization
- refund lifecycle design

Read:

- `references/retrieval-protocol.md`
- `references/standard-integration.md`

After drafting the solution, review it with:

- `references/review-checklist.md`
- `references/output-artifacts.md`

### Merchant Skill for OpenClaw Integration

Use this path when the user wants help with:

- OpenClaw-style merchant skill integration through `openclaw-payment-skills`
- merchant backend webhook support for email verification via `customer.verify`
- agent payment session design
- payment handoff contracts
- auto top-up or recharge recovery
- merchant confirmation flows
- `customer.verify` webhook handling

Read:

- `references/retrieval-protocol.md`
- run `node scripts/load_payment_skill_contexts.mjs --dependency openclaw-payment-skills --print-path`, then read the generated OpenClaw payment skill context
- `references/agent-integration.md`

After drafting the solution, review it with:

- `references/review-checklist.md`
- `references/output-artifacts.md`

### Merchant Skill for Generic Agent Integration

Use this path when the user wants help with:

- a merchant skill or merchant tool running inside a non-OpenClaw agent runtime
- a merchant or platform agent that is not tied to OpenClaw
- a generic agent runtime, third-party agent, custom orchestrator, or chat agent using `agentic-payment-skills`
- `clink-payment-skill` and `clink-cli` dependency design
- adapter design between the agent runtime and `agentic-payment-skills`
- merchant `402 Payment Required` handoff from a merchant API or tool into `agentic-payment-skills`
- callback, polling, queue, or recovery design for payment completion
- agent task resume behavior after merchant confirmation
- generic payment handoff contracts

Read:

- `references/retrieval-protocol.md`
- run `node scripts/load_payment_skill_contexts.mjs --dependency agentic-payment-skills --print-path`, then read the generated generic agent payment skill context
- `references/generic-agent-integration.md`

After drafting the solution, review it with:

- `references/review-checklist.md`
- `references/output-artifacts.md`

### Clink Documentation Dialogue

Use this path when the user wants help with:

- understanding or explaining official Clink docs
- answering doc-based product or API questions
- locating endpoint, field, webhook, or integration-contract details in official docs
- comparing an integration design against the documented contract

Read:

- `references/retrieval-protocol.md`
- the smallest relevant official-doc sections for the question

After drafting the answer, review it with:

- `references/review-checklist.md` when the question is about contract correctness

### Integration Validation

Use this path when the user wants help with:

- validating a merchant handoff contract
- checking whether a webhook design is production-safe
- generating a checklist, contract skeleton, or integration guidance artifact set
- validating required controls before implementation or launch

Read:

- `references/retrieval-protocol.md` when official docs are needed
- `references/validation-workflow.md`
- `references/output-artifacts.md`

After drafting the answer, review it with:

- `references/review-checklist.md`

## Working Method

- run doc-dependent work through `node scripts/load_official_docs.mjs`
- treat docs loading as a check-and-refresh gate, not as an unconditional refresh step
- for merchant skill for OpenClaw integration, run `node scripts/load_payment_skill_contexts.mjs --dependency openclaw-payment-skills --print-path` before generating code, integration guidance, or review output, then read the generated payment skill context
- for merchant skill for generic agent integration, run `node scripts/load_payment_skill_contexts.mjs --dependency agentic-payment-skills --print-path` before generating code, integration guidance, or review output, then read the generated payment skill context
- prefer the smallest set of local docs needed for the task
- route the request to the correct scenario before designing the flow
- read only the modules needed for the current task
- draft the scenario-specific solution first, then generate or review the output artifacts, then use `references/review-checklist.md` as the final self-review pass
- for new user onboarding, guide only from docs-confirmed account, dashboard, API key, product, webhook, and first checkout facts, then route the user to the appropriate implementation path
- if the user asks for implementation and no codebase is present, identify or ask for the backend language before writing code
- if the user asks for implementation guidance, help the coding agent decide what to build before attempting project-specific code
- for standard integration, clarify product mode before designing checkout creation
- for merchant skill for OpenClaw integration, separate merchant skill, merchant server, and `openclaw-payment-skills` responsibilities
- for merchant skill for generic agent integration, separate merchant skill or tool, agent runtime, adapter, merchant server, `agentic-payment-skills`, callback, and resume responsibilities
- when the user asks for developer help, prefer producing executable artifacts such as checklists, sample payloads, contract skeletons, and validation reports
- for validation tasks, prefer `node scripts/lint_contract.mjs`, `node scripts/lint_webhook_design.mjs`, and `node scripts/generate_guidance_artifacts.mjs`
- resolve the target environment before generating any code or configuration; use the resolved base URL in all generated code

## Hard Rules

- default all generated code and integration guidance to sandbox environment unless the user explicitly requests production
- keep new user onboarding guidance in sandbox even when the user mentions production; route production readiness or go-live onboarding requests through integration validation and production promotion instead of generating production onboarding directly
- use only "sandbox" and "production" as user-facing environment terms; do not expose internal naming such as "uat" or "prod" unless the output specifically targets developers who need the internal mapping
- do not generate production rollout guidance or production base URLs before the production validation gate completes successfully
- if the current task needs official docs, do not read or cite the cached official docs before running the freshness check command
- if the current task depends on `agentic-payment-skills` or `openclaw-payment-skills`, do not generate or review code from static memory alone; refresh and read the latest available payment skill context first
- running `node scripts/load_official_docs.mjs` means: use cache if it is within 7 days, refresh only if missing or older than 7 days, and fall back to stale cache only when refresh fails
- running `node scripts/load_payment_skill_contexts.mjs` means: download the latest GitHub codeload zip payment skill context into this skill's `.cache` when possible, never mutate sibling payment skill worktrees, and fall back to local sibling skill files only with an explicit warning
- do not mix standard integration, merchant skill for generic agent integration, and merchant skill for OpenClaw integration unless the user explicitly wants multiple paths
- do not treat `merchantReferenceId` as an idempotency key
- do not invent KYB, KYC, merchant approval, payout, production activation, or account setup steps beyond what the loaded official docs or maintainer-provided environment approval rules confirm
- for environment approval guidance, state that sandbox registration requires invite code `JUSTCLINK`, is automatically approved after registration, and succeeds, so users can obtain the sandbox Secret Key directly; production registration requires waiting for approval before production key or go-live guidance, and users can proactively contact support
- when asking the user to provide or configure a webhook signing key or Secret Key, state the dashboard path and method: webhook signing key comes from `Merchant Dashboard > Developers > Webhooks` after registering/selecting the webhook endpoint; Secret Key comes from `Merchant Dashboard > Developers > API Keys` by clicking `Initialize Key`, then copying and securely storing the key because it is displayed only once
- prefer environment variables or secret-manager placeholders for webhook signing keys and Secret Keys; do not ask the user to paste real secrets into chat, generated source code, docs, or public repositories
- do not describe webhook handling without dashboard subscription, endpoint registration, signature verification, idempotency, retry handling, and out-of-order tolerance
- do not assume a public refund-create API unless local docs explicitly show one
- do not describe merchant skill integration as a plain checkout redirect flow
- do not output final project-specific integration code unless the surrounding codebase and stack are known well enough
- do not answer a developer integration request with prose only when guidance artifacts or validation reports would materially help

## Module Map

- `references/retrieval-protocol.md`
- `references/new-user-onboarding.md`
- `references/standard-integration.md`
- `references/agent-integration.md`
- `references/generic-agent-integration.md`
- `references/output-artifacts.md`
- `references/validation-workflow.md`
- `references/review-checklist.md`
- `references/environment-strategy.md`

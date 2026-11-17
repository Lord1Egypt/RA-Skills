---
name: create-agent-app
description: Create or refactor production-grade TypeScript agent applications. Use when the user asks Codex to generate, scaffold, restructure, or harden a TypeScript agent app, including CLI agents, web agent apps, API services, internal tools, multi-agent harnesses, workflow-first systems, model provider wiring, tool registries, memory/state stores, safety policies, and validation gates.
---

# Create Agent App

Use this skill to turn a user request into a real TypeScript agent application base. Its purpose is to prevent toy demos and false validation claims.

## Required Flow

1. Read `references/grill-questions.md`.
2. Ask enough questions to produce an **Agent App Brief**. Do not scaffold yet.
3. Read the reference files that match the brief:
   - `references/architecture-patterns.md` for app and harness shape.
   - `references/provider-patterns.md` for model/provider wiring.
   - `references/harness-contract.md` for module boundaries and artifacts.
   - `references/safety-policy.md` for tools, approvals, credentials, and destructive actions.
   - `references/validation-policy.md` for verification requirements.
   - `references/official-docs.md` before coding against SDK or framework APIs.
   - `references/modern-selection-policy.md` before recommending "advanced" TypeScript, runtime, or agent-harness choices.
   - `references/industry-architecture-signals.md` when evaluating production architecture, observability, governance, scaling, or agent orchestration patterns.
   - `references/generation-contract.md` before implementing files.
4. Present the Agent App Brief plus 2-3 architecture candidates with concrete tradeoffs.
5. Present a brief-to-file mapping for the selected candidate: each major module must trace to a user requirement or safety/validation requirement.
6. Require explicit user confirmation of one candidate before editing files.
7. Generate or refactor the project with scoped, reviewable changes.
8. Run the agreed validation commands. Report the exact commands and real outcomes.

## Decision Gate

Do not create files, install packages, or scaffold until the user confirms:

- application type
- agent harness type
- runtime boundary and tool permissions
- model/provider pattern
- state and memory strategy
- safety policy
- validation standard

If the user explicitly says to use sensible defaults, still show the defaults and ask for confirmation before code generation.

## Non-Negotiable Rules

- Do not use silent fallback. If a provider, model, network call, tool, or permission fails, report the real failure and stop or ask for direction.
- Do not claim success for checks that were not run.
- Do not treat mocks, fake providers, or test doubles as implementation.
- Do not generate a chat box plus fake tool and call it an agent application.
- Do not write real credentials into source files. Use `.env.example` for variable names only.
- Do not enable destructive shell, delete, write, database mutation, browser automation, or external API mutation tools without an approval gate.
- Do not hide missing API keys. Mark live LLM validation as not run when credentials are unavailable.
- Keep `process.env` access centralized in `src/config/env.ts` and validate with `zod`.
- For current SDK or framework APIs, verify against official documentation before coding when the details may have changed.
- Do not stop at a partial demo. If the confirmed scope cannot be implemented, report the blocker instead of producing a decorative scaffold.
- Do not add "advanced" frameworks, agents, memory, queues, databases, or dashboards unless the brief justifies them.
- Treat "advanced" as current, official, typed, testable, observable, maintainable, and fit-for-purpose. Do not treat complexity as advanced.

## Expected Output

When generation is complete, return:

- chosen architecture and why it was selected
- changed files
- validation commands and outcomes
- live LLM smoke status
- remaining risks and next repair steps

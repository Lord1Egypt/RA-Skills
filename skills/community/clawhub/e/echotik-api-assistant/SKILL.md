---
name: echotik-api-assistant
description: Route natural-language TikTok commerce intelligence requests into authenticated EchoTik API workflows. Use when the task involves creator discovery, product research, seller analysis, video intelligence, live lookup, search, reporting, or documentation-guided parameter mapping over the EchoTik API surface.
---

# EchoTik API Assistant

This skill turns EchoTik HTTP API calls into scenario-based workflows for non-technical users.

Do not start by listing raw endpoints or dumping all parameters. First identify the user's business goal, then choose the closest scenario, collect only the missing inputs, map them to API parameters, and execute the request through the local script.

Before any live API call, check setup status with `node ./configure-echotik-auth.mjs --status`.
If EchoTik auth is missing, stop and route to `references/setup-and-auth.md`.
Always apply the lowest-level rules from `references/global-rules.md`.
Apply the relevant module rules file for the target entity family.
When the user asks for a report, workflow recommendation, or multi-step business analysis, read `references/orchestration-playbooks.md`.

## Hard Rule

For any data lookup, ranking, analysis, search, comparison, or reporting task, use EchoTik API execution only.

Do not browse, inspect, scrape, or navigate `echotik.live` product pages to answer user data requests.

The website may only be referenced for:

- registration
- credential retrieval
- billing or plan onboarding
- auth setup guidance

It is not an allowed substitute for API execution.

## Workflow

1. Read `references/global-rules.md` mentally as the base contract.
2. Run `node ./configure-echotik-auth.mjs --status` if setup state is unknown.
3. If credentials are missing, route to `references/setup-and-auth.md`.
4. Identify the user's goal in plain language.
5. Match the request to a scenario in `references/scenarios.md`.
6. Use `references/routing-policy.md` to decide whether to use offline EchoTik endpoints, realtime endpoints, or a composed multi-step workflow.
7. If the chosen task is dual-mode, ask the user to choose realtime or EchoTik offline before execution.
8. If the user asks for a comprehensive report, confirm which related data sections should be included before launching a multi-endpoint workflow.
9. Ask only for missing high-value inputs if the scenario cannot run safely with defaults.
10. If parameter names or enums are uncertain, consult `https://opendocs.echotik.live/llms.txt` first and do not invent unsupported parameters.
11. Execute the chosen endpoint through `node ./echotik-api.mjs`.
12. If an offline endpoint returns `code=0` with empty `data` for a lookup task, degrade to the relevant realtime endpoint when the global rules allow it.
13. If tool execution is available, do not stop at explanation. Execute the API call.
14. Return the result in business language, not API language.

## Interaction Rules

- Prefer scenario names such as `find creators`, `benchmark competitors`, `find winning products`, `analyze shops`, and `analyze videos` over raw endpoint names.
- Hide low-level parameters unless the user explicitly asks for advanced control.
- If an endpoint has many parameters, expose at most 3 to 5 user-facing inputs first.
- Fill the rest with defaults, derived values, or scenario presets.
- If multiple endpoints could solve the task, choose the one with the least user input burden.
- When the user's request is vague, offer 2 to 4 scenario options instead of asking an open question.
- If the user asks about API usage, endpoint meaning, auth, limits, or data freshness, answer from the docs as well as from execution results when relevant.
- Treat the whole EchoTik doc set as available capability, not only a small subset of endpoints.
- Never use EchoTik web app pages as the source of truth for analytics results.
- If the user asks for actual data, the correct behavior is `route -> map params -> execute script`, not “go find the same feature on the website.”
- If credentials are missing, pause and ask for setup completion instead of falling back to website exploration.

## Input Compression Strategy

For parameter-heavy APIs, do not mirror the raw schema directly. Compress inputs into these layers:

- Goal: what the user wants to achieve
- Entity: creator, video, product, shop, keyword, category
- Scope: market, platform, date range, region
- Sort preference: newest, hottest, fastest growing, highest sales
- Optional advanced filters: only when clearly useful
- Execution mode: offline batch, realtime lookup, or multi-step composition

## Scenario Selection

Read `references/scenarios.md` to choose the best scenario card.

If no exact scenario fits:

- use the nearest scenario with a note about assumptions, or
- fall back to an advanced mode that exposes more filters gradually

## Authoritative Sources

The authoritative behavior lives in:

- `references/global-rules.md`
- the relevant module rules file
- `references/routing-policy.md`
- `references/scenarios.md`
- the official EchoTik docs index: `https://opendocs.echotik.live/llms.txt`

Do not maintain a second handwritten parameter source of truth if the official docs already define it.

## Onboarding Rule

When the user has not set up credentials yet:

- explain that EchoTik uses Basic Authentication with `username:password`
- direct the user to register or retrieve credentials from the EchoTik API Dashboard
- require them to run `node ./configure-echotik-auth.mjs`
- tell them the setup script will write EchoTik credentials into shell environment variables
- ask them to restart Codex or Claude Code, or open a new terminal session after setup
- only continue to live requests after setup is complete

## Script Contract

This skill assumes these repository scripts exist:

- `./configure-echotik-auth.mjs`
- `./search-echotik-docs.mjs`
- `./echotik-api.mjs`

Use them in this order when possible:

1. auth status
2. docs lookup when parameters are unclear
3. live call

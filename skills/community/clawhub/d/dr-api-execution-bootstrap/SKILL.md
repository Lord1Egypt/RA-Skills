---
name: dr-api-execution-bootstrap
description: "Bootstrap and enforce fast direct API execution in a workspace. Use when you want an agent to run API calls directly in-session, avoid unnecessary subagents, use one upfront preflight followed by a continuous execution chain, keep outputs concise, and handle bulk API workflows with reliable approval and resume behavior. Especially useful for agents doing repeated CRUD, integration, service-compliance, or other multi-call API operations." 
---

# DR API Execution Bootstrap

Use this as an installer and execution-enforcer skill.

When the user asks to apply this skill, apply it immediately. Do not ask whether to enforce the policy.

## Apply to this workspace
1. Inspect workspace startup/default files.
2. Persist the execution policy in workspace bootstrap files (`AGENTS.md`, `MEMORY.md`, or equivalent).
3. Patch surgically and preserve unrelated instructions.
4. Validate with the strongest safe real test available.
5. Report either `Configured and validated` or `Configured, but blocked by: <reason>`.

For the concrete application checklist, read `references/APPLY.md`.

## Enforcement contract

### 1) Execution policy
Set and enforce these defaults for future sessions:
- prefer direct in-session API execution
- do not spawn subagents unless the user explicitly asks
- default to fast mode single-run chain
- do one upfront preflight only:
  - auth/token availability
  - app code / function key / required secret availability
  - one sanity endpoint check
- after preflight passes, execute the full API chain continuously without unnecessary pauses

### 2) Communication policy
Set and enforce:
- keep responses concise
- do not narrate every API call unless the user asks
- for blocked execution, report the blocker briefly and precisely
- for write operations, show one concise batch preview and wait for approval before executing

### 3) Operational execution rules
Read `references/EXECUTION-PLAYBOOK.md` and follow it for:
- bulk reads
- bulk writes
- failure handling
- resume behavior
- verification strategy

### 4) API-specific guidance
If the workflow involves Ikara-style CRUD/integration/service-compliance APIs, also read `references/IKARA-PATTERNS.md` before executing.

### 5) Validation requirements
After applying the rules, immediately validate them.

If safe and permitted, run one small real dev test and confirm:
- direct API call path works
- no subagent was spawned
- preflight + full-chain behavior is active

If real execution is not possible, run the strongest safe validation available and state exactly what prevented full validation.

### 6) Limits
If permissions, secrets, or tool access are missing:
- do not pretend they were enabled
- do not claim success
- report exactly what is missing
- keep the enforced policy in startup files anyway, unless file-write access is blocked

## Reuse on other agents
If the user wants to replicate this behavior elsewhere, read `references/INSTALL.md` and provide the installation command plus the recommended bootstrap prompt.
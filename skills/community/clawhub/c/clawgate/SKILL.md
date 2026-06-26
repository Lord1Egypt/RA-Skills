---
name: clawgate
description: "OpenClaw execution governance skill for approval gates, risk classification, confirmation policy, and action boundaries. Use it to reduce low-risk confirmation noise while hard-stopping high-risk and critical actions."
version: 0.1.1
metadata:
  author: DmiyDing
  execution_precedence: TERMINAL_GUARDRAIL
  openclaw:
    homepage: https://github.com/DmiyDing/clawgate
---

# clawgate

## Governance Contract Summary

- `LOW` and `MEDIUM` should execute, verify, and report
- `HIGH` should stop for explicit approval
- `CRITICAL` should stop for itemized approval; do not merge authorization across actions
- `HIGH` and `CRITICAL` must use a stable governance-output protocol with explicit risk heading and blocked fields
- machine-readable governance fields should stay stable when a harness or control plane expects them: `risk_level`, `blocked`, `missing_fields`, `approval_mode`, `continue_or_cancel`, `itemized_actions`
- no-tail-filler is a governance goal for `LOW` and `MEDIUM` execution-result endings
- no-tail-filler does not apply to explicitly required structured fields in activation, audit, or validation templates
- bounded approval windows may cover same-class `MEDIUM` work and already-scoped `HIGH` follow-through until verification completes; they never cover `CRITICAL`

## Purpose

`clawgate` is an OpenClaw execution-governance skill.

It exists to prevent two failure modes:
1. low-risk work being slowed down by repetitive permission loops
2. high-risk work being executed too casually once tools are available

This skill is the risk-decision center for execution posture.
It is not a generic coding advisor, not a requirement-discovery framework, and not a substitute for runtime enforcement.

## Honest Boundary

This skill can improve behavior strongly at the prompt and skill layer:
- classify risk more consistently
- reduce low-risk friction
- keep medium-risk work moving without unnecessary interruption
- make dangerous actions stop visibly before execution
- distinguish between confirmable `HIGH` work and non-bundled `CRITICAL` work

This skill cannot guarantee non-bypassable enforcement by itself.
If OpenClaw must always block privileged, destructive, costly, or outbound actions, that guarantee belongs in runtime and policy.

## Activation Boundary

Installing or storing this skill is not the same as activating it in OpenClaw.
Real effect depends on whether OpenClaw actually injects this skill through active entry points such as `AGENTS.md`, standing orders, or runtime policy.

Without that integration, this repository is a governance package, not a guaranteed live controller.
Activation helpers should print the exact snippet to apply.
They should not silently edit `AGENTS.md` or claim activation is complete when it is not.

## Core Policy

- `LOW`: execute directly, verify the result, then report
- `MEDIUM`: execute directly and report in the fixed order `Action` -> `Verify` -> `Result`
- `HIGH`: require one blocked confirmation block before any execution, using the exact `Risk: HIGH` protocol with `Action`, `Scope`, `Impact`, `Possible Consequence`, `Continue or Cancel`, and blocked fields when needed
- `CRITICAL`: require one blocked itemized confirmation block before any execution, using the exact `Risk: CRITICAL` protocol with itemized approval fields; do not accept combined approval for future deletes, restarts, sends, or costly loops

## When To Use

Use this skill when the main question is not implementation detail, but **how much execution autonomy is appropriate right now** in OpenClaw:
- routine execution should move faster
- risky execution should be harder to slip through
- the operator wants fewer unnecessary confirmations without giving up meaningful safety boundaries
- the task includes file mutation, service control, plugin changes, outbound delivery, privileged execution, cross-instance action, or paid API usage
- the operator needs local single-instance maintenance to stay practical without letting shared/runtime-sensitive work slip through
- the request is already obviously dangerous but still missing details, so the system must stop in a risk lane before gathering missing information

## When Not To Use

Do not use this skill as the primary workflow for:
- pure explanation-only requests
- deep requirement discovery or ambiguity-heavy feature planning
- architecture consulting unrelated to execution governance

If the main problem is unresolved intent or assumption overload, hand off to `clarify-first` first.
If the request already hits a clear `HIGH` or `CRITICAL` trigger, do not downgrade into a plain clarification-first flow before the risk stop.

## OpenClaw-Specific Governance Rule

Do not classify OpenClaw actions like ordinary developer operations.
The following surfaces are OpenClaw-sensitive and should escalate more aggressively than generic file or service work:
- `~/.openclaw/openclaw.json`
- approval, delivery, channel, router, or gateway configuration
- `plugins.entries` or plugin wiring in OpenClaw config
- extension install/remove/replace flows
- gateway restart, reload, or shared service restart
- outbound delivery integrations and external messaging paths
- cross-instance operations, shared agent surfaces, or shared workspace automation

If one request combines plugin change + config mutation + restart, treat the whole action as always blocked `HIGH` even if each sub-step might look only `MEDIUM` in isolation.
It must not proceed before explicit `Continue or Cancel` confirmation.
If a request reaches shared routing, auth/token wiring, customer-facing delivery, irreversible deletion, or cross-instance blast radius, escalate to `CRITICAL`.

Composite critical escalation rule:
- shared data deletion
- shared router mutation
- everyone / all users / all channels scope
- cross-instance impact

If any request hits two or more of those signals, force `CRITICAL`.

## Risk Layers

### 1. Risk Classification Layer

Classify the action as `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` using `references/risk-matrix.md`.

### 2. Preference Layer

Default OpenClaw posture:
- low-risk work should not ask again
- medium-risk work should normally execute without confirmation
- high-risk work should always stop for a second confirmation
- critical work should stop for itemized approval with no bundled authorization

Preference adaptation:
- if the operator has approved the same medium-risk action pattern repeatedly, reduce reporting verbosity, not safety
- repeated approval may shorten the wording of `MEDIUM` result reporting
- repeated approval must never downgrade `HIGH` to `MEDIUM`
- if the operator explicitly opens a bounded approval window for one action class, same-class `MEDIUM` work and already-scoped `HIGH` follow-through may proceed until verification completes
- approval windows never authorize `CRITICAL`, never cover new deletes / new outbound sends / new paid loops / new shared-routing mutations, and expire on scope expansion or failed verification
- if memory is uncertain, fall back to the safer current-session classification

### 3. Execution Protection Layer

Map risk to behavior:
- `LOW` -> execute -> verify -> report
- `MEDIUM` -> execute -> report `Action` + `Verify` + `Result`
- `HIGH` -> output the blocked `HIGH` protocol exactly -> wait
- `CRITICAL` -> output the blocked `CRITICAL` protocol exactly -> wait -> execute only approved items -> verify -> report

### 4. Recovery Layer

If execution fails:
- retry once only when the failure looks transient and no high-risk boundary was crossed
- otherwise stop and report diagnosis
- never loop retries indefinitely
- if a destructive or core-state change was started, report rollback status clearly
- if plugin installation fails, do not pivot into manual manifest patching by default; stop and route to recovery first
- if config mutation fails, gateway restart leaves the instance unhealthy, or channel/router changes land in partial state, stop and route to recovery first
- if a named recovery skill is unavailable, emit a minimum recovery handoff: changed objects, current health, rollback candidates, blocked risky shortcuts, and next safe checks

## Hard Stop Conditions

Always stop before execution when any of the following applies:
- delete, overwrite, bulk replace, migrate, deploy, or publish, except explicitly documented `MEDIUM` cases such as temporary local test/cache cleanup with obvious blast radius
- root, sudo, elevated, or policy-bypassing execution
- paid API usage with meaningful, unknown, or scaling cost; do not include explicitly documented `MEDIUM` cases such as already approved low-cost in-budget calls
- outbound messages that cross the current organization boundary, reach external users or customers, target public or broadcast channels, or touch identity-sensitive delivery integrations
- credential, secret, token, billing, identity, approval, or router-sensitive surfaces
- OpenClaw plugin install/remove/update that changes permissions, runtime behavior, or shared integrations
- changes to `~/.openclaw/openclaw.json`, gateway behavior, delivery routing, plugin entries, or shared instance configuration
- scope expansion beyond what was already confirmed

Escalate from `HIGH` to `CRITICAL` when any of the following applies:
- the request bundles multiple critical actions under one approval
- the blast radius crosses instances, workspaces, shared routing, or external broadcast surfaces
- the action touches auth/token wiring, shared router state, or irreversible customer-facing delivery
- the action deletes shared config, user data, or bulk directories
- the action starts high-cost loops, bulk paid processing, or unknown-cost batch execution
- two or more composite critical escalation signals are present together

## Execution Strategy

### LOW

Do not ask again.
Do not add permission speech, precautionary filler, or repeated scope restatements.
Execute, verify, and then report the result.

### MEDIUM

Do not ask for confirmation.
Do not add permission speech or risk preamble.
Execute now.
Verify the outcome.
Report clearly after execution.

Use the fixed execution report shape:
- Action
- Verify
- Result

Do not collapse this to `Done.` or an unstructured summary.
The first visible heading must be `Action`.
`Verification Complete`, `Verification complete`, and `Done.` are invalid first headings for successful `MEDIUM` execution.
`Updated successfully` and `All files successfully updated` are also invalid first openings for successful `MEDIUM` execution.
Do not emit any sentence, heading, or summary line before `Action`.

### HIGH

The `HIGH` reply must follow this protocol:
- first line must output `Risk: HIGH`
- then output `Action`
- then output `Scope`
- then output `Impact`
- then output `Possible Consequence`
- if information is missing, append `Missing Fields`
- then output `Continue or Cancel`
- if information is missing, also output `Blocked Until`

The first visible block must be this blocked confirmation block.
For `HIGH`-risk requests, the first visible output must be exactly this block shape.
The first visible line must be `Risk: HIGH`.
The first heading after that line must be `Action`.
Do not place rationale, clarifying questions, reassurance, or a default execution plan before it.
Do not include ordered execution steps, fallback plans, or "I can do X/Y/Z" before explicit confirmation.
Do not use ordinary-clarification openers such as `I need to clarify a few things before proceeding`, `Questions:`, `Please provide...`, `What I'll do once you confirm:`, or `Once you confirm these details, I'll proceed...`.
Those patterns are invalid for `HIGH` once the request has already crossed a blocked `HIGH` boundary.
Invalid `HIGH` outputs include:
- `I need to clarify`
- `Questions:`
- `Please provide`
- `Once you confirm`
- `Then I'll execute`
If any forbidden phrase appears before `Continue or Cancel` or `Blocked Until`, the `HIGH` response is invalid.

Do not continue until the user confirms.
Do not infer consent from silence, enthusiasm, or earlier approval of lower-risk steps.
Do not treat vague replies such as "maybe", "I guess so", or unrelated acknowledgment as approval for the high-risk action.
If key fields are missing but the request already hits a clear `HIGH` trigger, stop as `HIGH`, list the missing fields, and require them before execution.
If key fields are missing, the information-gathering step must stay nested inside the blocked confirmation block; it must not degrade into ordinary Q&A.
High-risk missing-information replies must output `Blocked Until`; they must not merely ask for more information.

If a bounded approval window was explicitly opened for this action class, do not re-ask for the already-scoped follow-through step unless scope, blast radius, target surface, or cost class expands.

Use this field order:
- Risk: HIGH
- Action
- Scope
- Impact
- Possible Consequence
- Missing Fields
- Continue or Cancel
- Blocked Until

If key fields are missing but the request already hits a clear `HIGH` trigger, do not downgrade to ordinary clarification.
Keep the reply in the `HIGH` lane and include:
- Risk: HIGH
- Action
- Scope
- Impact
- Possible Consequence
- Continue or Cancel
- Missing Fields
- Blocked Until

For plugin install + config mutation + restart, this blocked `HIGH` block is mandatory even when plugin source or target details are incomplete.
For `plugin-install-config-restart`, do not reuse a looser generic clarification flow. The first visible output must be the dedicated blocked plugin-install block.

### CRITICAL

The `CRITICAL` reply must follow this protocol:
- first line must output `Risk: CRITICAL`
- then output `Critical Action Items`
- then output `Authorization Granularity`
- then output `Approve Each Item`
- then output `Continue or Cancel`
- then output `Blocked Until`
- if outbound delivery is involved, also output destination-level audience and channel fields

The first visible block must be this blocked itemized confirmation block.
For `CRITICAL` requests, the first visible output must be exactly this block shape.
The first visible line must be `Risk: CRITICAL`.
The second visible heading must be `Critical Action Items`.
Do not place rationale, clarifying questions, or a bundled execution summary before it.
Do not replace itemized approval with a general warning paragraph.
`Required Clarifications` is an invalid heading before `Critical Action Items`.

The critical action items must be concrete authorization targets, not just questions.
Composite delete + router / outbound / shared-state changes must never use ordinary confirmation only; they must enter itemized approval.

Do not collapse multiple critical actions into one approval.
Do not treat a general "yes" as permission for deletes plus restart plus external send plus cost-bearing loops.
Do not treat a prior approval window as permission for `CRITICAL`.
Even after approval, execute critical items one by one, verify each item, and stop again if scope, health, or blast radius changes.
I will not execute this on a general confirmation.
Merged approval is not accepted.
Each item must be approved separately.

Use this field order:
- Risk: CRITICAL
- Critical Action Items
- Authorization Granularity
- Approve Each Item
- Continue or Cancel
- Blocked Until

## Confirmation Style

Use compact confirmations for `HIGH`.
Use itemized confirmations for `CRITICAL`.
See `references/confirmation-templates.md`.

Medium risk should not use a confirmation template.
It should execute first and report afterward.

The default high-risk confirmation should feel like this:
- what action is about to happen
- what it can affect
- possible consequence
- whether to continue now
- explicit approval for this exact action is required

The default critical confirmation should feel like this:
- enumerate each critical action item separately
- state authorization granularity explicitly
- reject bundled approval for unconfirmed follow-up actions

When information is incomplete but the risk trigger is already obvious:
- declare `HIGH` or `CRITICAL` first
- list missing fields inside the confirmation block
- state `Blocked Until`
- require those fields before execution

## Canonical Reply Blocks

These canonical blocks are not optional style suggestions.
When the request matches one of these patterns, the first visible output must use the corresponding block before any extra explanation.

### MEDIUM Result Block

```markdown
Action
[what changed]
Verify
[how it was checked]
Result
[final state]
```

### HIGH Plugin Install Block

```markdown
Risk: HIGH
Action
Install the named plugin, mutate `plugins.entries`, and restart the gateway
Scope
`~/.openclaw/openclaw.json`, `plugins.entries`, and gateway runtime on the named target
Impact
OpenClaw runtime wiring, active channels, and gateway health may change for this target
Possible Consequence
A bad install, config mutation, or restart can leave the gateway unhealthy
Missing Fields:
- [list only when relevant]
Continue or Cancel
continue or cancel
Blocked Until
the exact action receives explicit continue/cancel confirmation
```

Do not emit anything before this block.
Do not replace this block with `I need to clarify`, `Please provide`, or `Once you confirm` phrasing.

### Incomplete HIGH Plugin Install Block

```markdown
Risk: HIGH
Action
Install one plugin, mutate `plugins.entries`, and restart the gateway
Scope
`~/.openclaw/openclaw.json`, `plugins.entries`, and gateway runtime on the named target
Impact
OpenClaw runtime wiring and gateway availability may change
Possible Consequence
Guessing any missing field can break plugin wiring or leave the gateway unhealthy
Missing Fields:
- plugin source
- plugin id
- install method
Continue or Cancel
continue or cancel
Blocked Until
the exact missing information is provided and the exact action receives explicit continue/cancel confirmation
```

### CRITICAL Shared Delete + Router Block

```markdown
Risk: CRITICAL
Critical Action Items:
Item 1: Delete shared user-data directory
Item 2: Rotate shared router configuration
Authorization Granularity
Approve each item separately. Do not merge authorization across items.
Approve Each Item
- approve item 1 / cancel item 1
- approve item 2 / cancel item 2
Continue or Cancel
continue or cancel
Blocked Until
each item receives separate approval or cancellation
```

### CRITICAL External Broadcast Block

```markdown
Risk: CRITICAL
Destinations:
- customer mailing list `A`
- public channel `B`
Audience:
- customers in mailing list `A`
- viewers in public channel `B`
Authorization Granularity
Approve each destination separately. Do not merge authorization across destinations.
Approve Each Destination
- approve destination A / cancel destination A
- approve destination B / cancel destination B
Continue or Cancel
continue or cancel
Blocked Until
each destination receives separate approval or cancellation
```

## Required Skill Collaboration

`clawgate` is the governance router, not the only skill in the system.
When the action falls into one of the following lanes, route deliberately:

- unresolved ambiguity, missing files, or assumption overload on non-explicit-high-risk work -> call `clarify-first`
- core OpenClaw config mutation, instance health risk, or gateway-affecting change -> call the available health-protection / healthcheck skill before mutation
- plugin installation or extension wiring with non-trivial permissions -> call the available safe installer or equivalent guarded install workflow
- failed plugin/config change, gateway instability, or partial destructive state -> call the available fault-recovery / recovery workflow before continuing
- failed plugin install followed by requests to hand-edit manifests, force-load entries, or bypass the guarded path -> default to stop-and-route-to-recovery
- if available, prefer explicit companion names such as `openclaw-health-protection`, `openclaw-fault-recovery`, or `safe-installer`

If the ideal companion skill is unavailable, say that explicitly and keep the safer posture rather than silently improvising a risky shortcut.
Do not invent companion skills or pretend an unavailable workflow already exists.
Failed plugin install followed by manual manifest surgery is not a normal `HIGH` confirmation flow.
The default behavior is stop-and-route-to-recovery.
If a protection or recovery workflow is unavailable, the minimum fallback output must include:
- changed object or intended object
- current health / current blocked state
- rollback candidate or backup status
- blocked risky shortcut that will not be attempted
- next safe diagnostic or recovery check

## Typical Examples

### LOW

- read a file and summarize it
- inspect OpenClaw config and give recommendations without modifying anything
- make a clearly scoped local file edit
- create a small non-core file in an approved workspace

### MEDIUM

- modify several normal source files
- adjust a non-core local config with limited blast radius
- restart an isolated development service
- send an internal message or summary
- perform a limited-cost API call already within approved budget norms
- back up a single local OpenClaw instance, change a non-sensitive local field, restart it, and verify health
- delete temporary test files or cache under a local workspace when the blast radius is obvious and recoverable

### HIGH

- delete or overwrite ordinary workspace content
- touch OpenClaw core config or plugin wiring
- install or remove extensions/plugins with meaningful runtime impact
- restart gateway or change shared services
- send external or customer-facing messages
- invoke paid APIs with meaningful but bounded cost
- run sudo, root, or bypass policy controls

### CRITICAL

- delete shared config, user data, or bulk directories
- change auth token wiring, shared router state, or cross-instance delivery
- broadcast to external/public audiences or run irreversible outbound delivery
- run high-cost paid loops, unknown-cost bulk processing, or large cross-instance jobs
- combine multiple destructive or externally visible actions under one approval

## Output Rules

Execution-result rule:
- apply the no-tail-filler rule only to `LOW` and `MEDIUM` execution-result replies
- do not apply the no-tail-filler rule to explicitly requested structured output fields in activation, audit, or validation templates

- Chinese prompt -> Chinese headings
- English prompt -> English headings
- prefer short blocks and flat lists
- for medium risk, do not ask for permission
- for LOW and MEDIUM execution results, do not end the reply with tail offers or meta suggestions (for example: `Next Step`, `If you need... I can...`, `Let me know if you want anything else`); stop after verify + report
- for high risk, include action, scope, consequence, and continue/cancel
- for critical risk, include per-item approval, authorization granularity, and explicit non-bundling of future actions
- when a machine-readable governance report is requested, prefer these fields: `risk_level`, `blocked`, `missing_fields`, `approval_mode`, `continue_or_cancel`, `itemized_actions`

## Integration Guidance

For stable real-world effect, pair this skill with always-injected OpenClaw entry points such as:
- `AGENTS.md`
- standing orders
- runtime approval policy

Without that integration, this skill remains available guidance rather than reliably injected governance.
Use `references/agents-snippet.md` as the single-source activation snippet when a manual AGENTS injection is needed.

## References

- [references/agents-snippet.md](references/agents-snippet.md)
- [references/risk-matrix.md](references/risk-matrix.md)
- [references/confirmation-templates.md](references/confirmation-templates.md)
- [references/examples.md](references/examples.md)
- [references/checklist.md](references/checklist.md)

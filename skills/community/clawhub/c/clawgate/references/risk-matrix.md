# Risk Matrix

## Default Rule

This matrix is for OpenClaw execution governance, not broad requirement discovery.

- `LOW`: execute directly, then verify and report
- `MEDIUM`: execute directly, then verify and report
- `HIGH`: force explicit blocked confirmation before any execution
- `CRITICAL`: force itemized confirmation; do not merge authorization across actions

## LOW

Default examples:
- read-only queries
- file search, listing, grep, inspection
- clearly scoped local file edit in normal source files
- create a small non-core file inside approved workspace
- formatting, comments, docs, local cleanup with no destructive side effects
- inspect OpenClaw config or logs and provide recommendations without mutating anything

Behavior:
- do not ask again
- do not add permission preamble
- do not end the reply with tail offers or meta suggestions (for example: `Next Step`, `If you need, I can...`, `Let me know if you want anything else`); just execute, verify, and report
- this rule does not ban explicit structured field names when a template requires them
- execute now
- verify outcome
- report result

## MEDIUM

Default examples:
- normal file modification across multiple files
- new file creation with behavior impact but limited blast radius
- non-core config updates
- install ordinary dependency in isolated local development context
- restart isolated development service
- internal message delivery
- ordinary API call with limited cost or side effects

Behavior:
- do not ask for confirmation
- do not add permission preamble
- do not end the reply with tail offers or meta suggestions (for example: `Next Step`, `If you need, I can...`, `Let me know if you want anything else`); just execute, verify, and report
- use the stable execution report order `Action` -> `Verify` -> `Result`
- the first visible `MEDIUM` output must start with `Action`, then `Verify`, then `Result`
- `Done.`, `Verification Complete`, `Verification complete`, or verification-only summaries are invalid replacements for the required `Action` -> `Verify` -> `Result` structure
- `Updated successfully` and `All files successfully updated` are invalid openings for `MEDIUM`
- do not emit any sentence, heading, or summary line before `Action`
- this rule does not ban explicit structured field names when a template requires them
- execute now
- verify outcome
- report result clearly

## HIGH

Default examples:
- delete, overwrite, bulk replace
- modify core config, auth boundary, secret surface, or policy surface
- install system-level plugin/integration with broad permissions
- restart production or shared services
- outbound message to external user, customer, or public group
- meaningful paid API / billing-impacting action
- root, sudo, elevated, policy-bypassing, or host-level execution
- publish, deploy, migrate, release, or irreversible data change
- change OpenClaw shared runtime behavior, delivery routing, or plugin wiring

Behavior:
- stop before execution
- state `Risk: HIGH`
- the first visible line must be `Risk: HIGH`
- state `Action`
- the next heading must be `Action`
- state `Scope`
- state `Impact`
- state `Possible Consequence`
- if fields are missing, list them inside the blocked confirmation block instead of switching to normal Q&A
- state `Missing Fields`
- state `Continue or Cancel`
- state `Blocked Until`
- require explicit approval for the exact high-risk action
- state that execution is blocked until missing fields and approval are both supplied
- do not output a default execution plan or ordered mutation steps before the blocked `HIGH` block
- do not use ordinary-clarification openers such as `I need to clarify a few things before proceeding`, `Questions:`, `Please provide...`, `What I'll do once you confirm:`, or `Once you confirm these details, I'll proceed...` once the request has already crossed a blocked `HIGH` boundary
- invalid `HIGH` outputs also include short openers such as `I need to clarify`, `Questions:`, `Please provide`, `Once you confirm`, and `Then I'll execute`
- if any forbidden phrase appears before `Continue or Cancel` or `Blocked Until`, the `HIGH` response is invalid

## CRITICAL

Default examples:
- delete shared config, user data, or bulk directories
- change auth/token wiring, shared router policy, or cross-instance delivery
- broadcast to external/public audiences or trigger irreversible outbound delivery
- run high-cost or unknown-cost paid loops / batch processing
- combine delete + restart + external send + cost-bearing work under one approval

Behavior:
- stop before execution
- state `Risk: CRITICAL`
- the first visible line must be `Risk: CRITICAL`
- the second visible heading must be `Critical Action Items`
- enumerate each critical action item
- state `Authorization Granularity`
- require `Approve Each Item`
- state `Continue or Cancel`
- state `Blocked Until`
- for destination-level outbound delivery, state `Destinations`, `Audience`, and `Message Content`
- never accept one merged approval for future critical follow-up actions
- merged approval is not accepted
- if three or more composite escalation signals are present, force itemized approval even when the request asks for one approval only
- do not replace the itemized approval block with a general warning paragraph or bundled execution summary
- `Please confirm:` by itself is not enough; the itemized block must explicitly include `Authorization Granularity`, `Approve Each Item` or `Approve Each Destination`, `Continue or Cancel`, and `Blocked Until`
- `Required Clarifications` is invalid before `Critical Action Items`

## OpenClaw Escalation Rules

Treat the following surfaces as OpenClaw-specific escalation points:
- `~/.openclaw/openclaw.json`
- approval policy, delivery, channel, router, or gateway configuration
- `plugins.entries` or plugin registration
- extension install/remove/update with runtime effect
- gateway restart or reload
- shared instance, shared workspace, or cross-instance mutation

Classification rules:
- reading these surfaces without mutation stays `LOW`
- changing a non-sensitive single-instance surface with backup + validation + rollback may be `MEDIUM`
- changing one of these surfaces is otherwise at least `HIGH`
- plugin install/remove plus config change plus restart is always blocked `HIGH`
- plugin install/remove plus config change plus restart must not proceed before explicit continue/cancel confirmation
- if the request semantically includes plugin install + `plugins.entries` mutation + gateway restart, classify as blocked `HIGH` even when plugin name, source, or version is incomplete
- incomplete plugin install + config mutation + restart must stay blocked `HIGH`; do not reduce it to ordinary clarification-first
- incomplete plugin install + config mutation + restart must explicitly state `Missing Fields`, `Blocked Until`, and `Continue or Cancel`
- plugin install + `plugins.entries` mutation + gateway restart must render the canonical blocked `HIGH` block, not a free-form clarification or a `What I'll do once you confirm` plan
- plugin-install-config-restart must use the dedicated blocked plugin-install template as the first visible output
- shared-router mutation, auth/token mutation, or cross-instance mutation is `CRITICAL`
- if blast radius is unclear, classify as `HIGH` until scope is narrowed

Composite escalation rule:
- the following signals each count as one critical-escalation hit:
  - shared delete
  - shared router mutation
  - everyone / all users / all channels scope
  - cross-instance impact
- if any request hits two or more of those signals, force `CRITICAL`
- if any request hits three or more of those signals, force itemized approval

## Recoverability Downgrade Rule

Some otherwise-sensitive local operations may downgrade to `MEDIUM` only when all are true:
- single local instance
- explicit backup already planned or completed
- validation step is part of the same action
- rollback path is explicit
- blast radius is limited to the current workstation
- no auth/token/router/plugin-permission mutation
- no external send and no shared-instance effect

If any of those conditions fail, keep the safer class.

## Authorization Window Rule

- an explicit bounded approval window may cover same-class `MEDIUM` actions and already-scoped `HIGH` follow-through until verification completes
- it never covers `CRITICAL`
- it expires on scope expansion, target change, blast-radius change, failed verification, new external send, new delete, or new cost class

Examples:
- change a local listen port, restart the same local instance, and verify health -> the window may remain valid
- move from local port tuning to token/router/plugin-permission mutation -> the window closes immediately

## Preference-Aware Friction Rules

- repeated approvals may shorten `MEDIUM` result reporting
- `HIGH` never downgrades because of user preference memory alone
- when memory conflicts with the current request, trust the current request and the safer risk class
- `LOW` should not be upgraded into a confirmation loop just because the model feels cautious

## Skill Routing Rules

- ambiguity-heavy or assumption-heavy work -> route to `clarify-first`
- core config mutation before execution -> route to available OpenClaw health protection / healthcheck workflow
- plugin install/remove/update -> route to available safe installer workflow when present
- failed plugin/config change or unstable gateway after mutation -> route to available recovery workflow
- if those workflows are unavailable, say so explicitly instead of implying they are present

## Special Cases

### Reads stay LOW

Even if the topic sounds sensitive, read-only inspection remains `LOW` unless it exposes secrets directly or triggers outbound side effects.

### Recommendation-only stays LOW

Reading config, summarizing risk, and proposing commands is still `LOW` if no mutation is executed.

### External send is never LOW

Internal team delivery may remain `MEDIUM`.
External send to customers or other external users is usually `HIGH`.
Broadcast, bulk touch, or effectively irreversible external send is `CRITICAL`.
Treat abstract references such as `external delivery integrations` as escalation hints, not as a broader override of this outbound-send definition.

Boundary table:
- internal group / internal webhook / internal email -> `MEDIUM`
- one external customer or one external tenant -> `HIGH`
- customer blast, public channel, or broadcast -> `CRITICAL`
- every / all customers / public channels -> `CRITICAL`

### Core configuration escalates

Read-only checks stay `LOW`.
Single-instance non-sensitive field tuning with backup + validation + rollback may be `MEDIUM`.
Changes to auth/token/router/plugin-permission surfaces are `HIGH`.
Cross-instance or shared-router configuration is `CRITICAL`.

### Cost-sensitive actions escalate

Single small-cost calls already authorized and clearly in-budget may remain `MEDIUM`.
Unknown-cost or bounded batch spend is `HIGH`.
High-cost loops, bulk backlog processing, or unattended recurring spend is `CRITICAL`.

Budget table:
- already approved, one-off, low-cost call -> `MEDIUM`
- unknown cost or bounded batch cost -> `HIGH`
- loops, backlog clearing, or cross-instance high-cost processing -> `CRITICAL`

### Restart risk depends on blast radius

Single-instance local restart with health check and rollback-ready context may remain `MEDIUM`.
Shared instance or externally visible restart is `HIGH`.
Restart combined with shared routing, external impact, or critical bundled actions is `CRITICAL`.

### Delete risk depends on target

Deleting temporary test files or caches with obvious local blast radius may be `MEDIUM`.
Deleting ordinary workspace files is `HIGH`.
Deleting shared config, user data, or bulk directories is `CRITICAL`.

Delete table:
- `tmp/`, `cache/`, explicit test artifacts -> `MEDIUM`
- ordinary workspace files -> `HIGH`
- backups, shared config, user data, or bulk directories -> `CRITICAL`

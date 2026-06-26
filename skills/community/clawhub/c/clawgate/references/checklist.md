# Execution Checklist

## Before Classifying

- Is this request about execution governance rather than broad requirement discovery?
- Is the task read-only, mutating, external, privileged, cost-sensitive, or cross-instance?
- Does the action touch normal files, core config, services, plugins, secrets, outbound delivery, gateway, or system surfaces?
- Is this an OpenClaw-sensitive surface that should escalate faster than an ordinary developer workflow?
- Is this single-instance local maintenance with explicit backup, validation, and rollback, or does it cross into shared/runtime-sensitive territory?

## LOW Check

Proceed directly only if all are true:
- scope is explicit enough
- no destructive action
- no outbound send
- no paid or privileged action
- no core runtime, shared instance, or secret mutation
- no plugin install/remove/update
- no need for extra permission wording once risk remains `LOW`

## MEDIUM Check

Direct-execute as `MEDIUM` if any are true:
- multiple file edits with limited blast radius
- new behavior but not core runtime/policy
- internal send or limited-side-effect API call
- install dependency in isolated development context
- restart isolated development service
- single-instance local OpenClaw maintenance with backup + validation + rollback and no auth/router/plugin-permission mutation
- delete temporary test files or cache with obvious local-only blast radius

Execution rule:
- do not ask for confirmation
- do not add permission preamble
- execute directly
- verify result
- report clearly

## HIGH Check

Force second confirmation if any are true:
- delete ordinary workspace content, overwrite non-temporary content, migrate, deploy, or publish
- outbound messages that cross the current organization boundary, reach external users or customers, target public or broadcast channels, or touch identity-sensitive delivery integrations
- sudo / root / elevated / bypass policy
- paid API usage with meaningful but bounded cost, or any cost whose exact spend is still unclear
- core config / auth / secret / delivery-routing surface
- `~/.openclaw/openclaw.json` mutation
- `plugins.entries` mutation or extension install/remove/update
- gateway restart, reload, or shared service change
- cross-instance or shared-workspace mutation
- non-broadcast external send to customers or external users
- bounded but meaningful paid API usage

Approval rule:
- require explicit approval for this exact action
- do not execute on silence, vague acknowledgment, or approval meant for a lower-risk step
- a bounded approval window may cover only already-scoped follow-through inside the same action class

## CRITICAL Check

Force itemized confirmation if any are true:
- delete shared config, user data, or bulk directories
- touch auth token wiring, shared router state, or cross-instance delivery
- run broadcast / bulk / effectively irreversible external send
- start unknown-cost or high-cost paid loops / bulk processing
- combine multiple destructive, externally visible, or costly actions under one approval

Approval rule:
- require per-item approval
- state authorization granularity explicitly
- do not merge authorization for later restart / delete / external send / paid loop steps
- approval windows never cover `CRITICAL`

## Routing Check

- ambiguity or assumption overload -> `clarify-first`
- core OpenClaw config change -> health protection / healthcheck workflow first
- plugin install/remove/update -> guarded installer workflow first
- failed mutation, unstable gateway, or partial destructive state -> recovery workflow first
- if a named guarded workflow is unavailable, say that directly and stay conservative
- failed plugin install followed by requests to hand-patch manifest or force the install -> default to stop-and-route-to-recovery
- failed config change, unhealthy gateway after restart, or half-applied channel/router mutation -> default to stop-and-route-to-recovery
- if no recovery skill exists, output minimum recovery actions: changed object, current health, rollback candidate, blocked risky shortcut, next safe check

## Activation Check

- installing the skill is not the same as activating it
- if AGENTS or standing-order injection is still needed, output the exact snippet and target path
- do not auto-edit `AGENTS.md` unless the user explicitly requested that exact mutation

## Preference Check

- if the user has approved similar medium-risk actions repeatedly, reduce result verbosity rather than reintroducing permission friction
- do not let preference memory downgrade `HIGH`
- if the user explicitly opened a bounded approval window, keep it scoped to the named action class and stop using it once verification completes or scope expands
- if memory is stale or uncertain, use the safer present-time classification

## After Execution

- verify the result, not just the action
- report what changed
- LOW/MEDIUM tail-filler check: do not end the reply with meta offers like `Next Step`, `If you need...`, `I can help...`, or `Let me know...`; stop after verify + report
- tail-filler scope rule: apply this only to LOW/MEDIUM execution-result replies, not to explicitly required structured fields in activation or audit templates
- if anything deviated from expected scope, say so explicitly
- if a destructive action failed halfway, report rollback status
- if OpenClaw shared state was touched, say whether instance health still looks normal
- for MEDIUM/HIGH/CRITICAL operational work, prefer a fixed post-execution report with: changed object, executed action, verification result, rollback status, instance health

## Tail-Offer Review Examples

Disallow endings like:
- `Next Step: tell me if you want me to continue.`
- `If you need, I can also handle the next part.`
- `Let me know if you want anything else.`
- `下一步我也可以继续帮你处理。`
- `如果需要我可以顺手一起做掉。`
- `I would suggest tackling the next part now.`
- `To make this land better, you can let me continue with the follow-up.`
- `我建议下一步把后续也一起做完。`
- `为了更好落地，我可以继续帮你把下一段处理掉。`

Allow endings like:
- `Updated 3 files. Verified the logger calls compile cleanly.`
- `已修改 3 个文件，验证通过，未发现额外漂移。`
- structured activation or audit fields explicitly requested by template, such as `Activation Status` or `Next Step`

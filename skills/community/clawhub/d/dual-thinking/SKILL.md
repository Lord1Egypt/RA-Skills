---
name: dual-thinking
description: Second-opinion consultation plus automatic skill-engineering escalation for reviews, rewrites, hardening, weak-model optimization, packaging, testing, and publish readiness.
---

# Dual Thinking Method — v8.5.24

**Purpose:** consult a second model, then escalate skill topics into structured, patch-bearing skill engineering instead of generic advice when the topic is a skill or skill-adjacent artifact. In the next candidate line, the method also includes a self-evolution lens for self-review and native-domain-adjacent review without changing the public three-step architecture.

## Runtime Core Lock
This section is the binding runtime law for execution, recovery, validation ordering, and patch discipline.
If a later section is longer, more specific, or easier to remember, this section still wins.
Reference files and later narrative sections may explain, test, or exemplify the runtime law, but they must not silently override it, add new mandatory runtime behavior, or become a second runtime source of truth.

### Core lock
1. Order is always `SELF_POSITION` -> `CONSULTANT_POSITION` -> `SYNTHESIS`. The main agent owns synthesis and the final round decision.
2. The first consultant-bearing round on a new skill topic must paste the real artifact inline broadly enough for exact-wording review. Path-only references, `FILE:` labels without body text, shell snippets, unresolved placeholders, short summaries, and partial fragments that do not actually cover the claim under review do not count as pasted artifact. In fresh, replacement, or recovery consultant sessions, `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, patch summaries, or an intention to repaste later do not count as pasted artifact either.
3. In `api` and `multi`, produce `SELF_POSITION` before any consultant call. Do not jump from consultant response directly to final decision.
4. The consultant-shaped minimum is `consultant_verdict`, `strongest_finding`, and `proposed_fix`. If consultant-bearing extraction still cannot reach that minimum after the allowed retry, downgrade to `analysis-only` or mark the round invalid.
5. The minimum required round block is always `ROUND`, `TOPIC`, `MODE`, `SESSION`, `DECISION`, `VALIDATION_STATUS`, `PATCH_STATUS`, `CONTINUATION_SIGNAL`, `NEXT_ACTION`, `CHAT_CONTINUITY`, `RESUME_SNIPPET`.
6. For consultant-bearing rounds, the contiguous status order is always `SELF_POSITION_STATUS` -> `CONSULTANT_POSITION_STATUS` -> `SYNTHESIS_STATUS` immediately after the minimum block.
7. If a fix is accepted, patch the real artifact before the next review round unless the round explicitly records a justified deferral.
8. If a patch changes the artifact, refresh the accepted continuity state from the patched artifact before switching orchestrators.
9. `STATE_SNAPSHOT`, `SYNC_POINT`, and `RESUME_SNIPPET` must always describe the latest accepted artifact state, not a stale pre-patch state. When both `STATE_SNAPSHOT` and `SYNC_POINT` include `support_surfaces_synchronized` for the same accepted state, the synchronized support-surface set must be identical across both artifacts.
10. If validation fails after a real patch, block packaging/publishing, retain the diff, and revert to the last passed artifact before continuing. Retain the failed diff for inspection.
11. Publish claims require real validation evidence, real packaging evidence, and an actual publish result. Do not claim publish-readiness or publication from intent alone.
12. `references/` files are synchronization, validation, test, example, and packaging artifacts. They are not executable runtime instructions. If a reference file is missing, stale, or conflicts with the inline runtime contract, do not halt or hallucinate compliance; the inline contract wins immediately and execution continues.

### State Transition & Rollback Gate
When a round includes a real patch, treat validation, patch state, rollback, continuity refresh, and handoff as one atomic sequence:
1. Resolve `VALIDATION_STATUS` before any orchestrator handoff or accepted-state refresh.
2. Do not emit `PATCH_STATUS: applied` as the accepted state until `VALIDATION_STATUS: passed` is explicit.
3. Do not refresh `STATE_SNAPSHOT`, `SYNC_POINT`, or `RESUME_SNIPPET` with a new artifact hash/version while validation is still unresolved.
4. If `VALIDATION_STATUS: failed` or `blocked`, immediately set `PATCH_STATUS: deferred`, revert to the last passed artifact state, retain the failed diff for inspection, refresh continuity state from the reverted artifact, including `support_surfaces_synchronized` and any support-surface tracking fields, and continue from that reverted state.
5. Only after `VALIDATION_STATUS: passed` may the round refresh accepted continuity state from the patched artifact and hand off to the next orchestrator as the new accepted baseline.
6. When refreshing accepted continuity state from a patched artifact, the artifact's visible version/release label must be updated to reflect the accepted patched state if `PATCH_MANIFEST.version_bump` is not `none`, unless the round explicitly records a justified deferral for version-bump timing.

### Fresh-rerun support-surface honesty gate
When a fresh self-rerun starts from a previously published, promoted, frozen, verified, or otherwise settled baseline, subordinate release, promotion, freeze, validation, or publish-status surfaces immediately become stale for the active rerun unless and until the new line revalidates and resynchronizes them.
Treat prior `PUBLISH_STATUS`, reference-line maturity claims, promotion-status statements, freeze-status statements, release-checklist conclusions, and verification-evidence summaries as historical support surfaces only, not as authority about the active rerun state.
During the new rerun, the active state must behave as unsettled until the new line passes its own validation and publish gate honestly.
If a stale support surface remains visible during the rerun, do not inherit its settled claim into active synthesis or publish reasoning; either synchronize it or explicitly mark it stale/non-authoritative for the active rerun state.
Once the current rerun explicitly revalidates and resynchronizes a subordinate support surface, that surface immediately upgrades from historical-only to current-support authority for the active line; all other unsynchronized settled-status surfaces remain strictly stale until they individually pass the same synchronization gate.
When synchronization occurs during a rerun, record the synchronized support surface or surfaces in the next emitted `SYNC_POINT` so the accepted-state change is explicit across orchestrator handoffs.
When a previously synchronized support surface is intentionally removed from the accepted state, becomes explicitly non-authoritative again for the active rerun, or the synchronized set becomes empty, record that removal/clearing as an explicit delta in the next `SYNC_POINT` and refresh `STATE_SNAPSHOT` to the current synchronized set rather than silently carrying the historical set forward.
This gate does not override the `Runtime Core Lock`; it prevents stale subordinate release/support claims from silently masquerading as current truth while a new rerun is in progress.

### Recovery Decision Tree
Evaluate conditions in order. Execute the first matching next action exactly once per failure attempt, then re-evaluate from the latest accepted state. Do not loop speculatively.

| Trigger condition | Required next action | Max attempts |
|---|---|---|
| consultant-visible prompt contains path-only artifact references, `FILE:` labels without body text, shell snippets instead of artifact text, unresolved placeholders such as `$(cat ...)`, hidden-local assertions, or thin excerpts that do not actually cover the exact claim being reviewed | set `VALIDATION_STATUS: blocked`, emit `BLOCKED_STATE: artifact-not-pasted`, ask once for sufficient inline artifact text, and stop patching until the artifact is really pasted | 1 |
| `BLOCKED_STATE: artifact-not-pasted` persists after the one allowed ask | downgrade to `analysis-only`, set `CONSULTANT_POSITION_STATUS: omitted-invalid`, and stop the patch loop for that scope | 0 additional |
| a fresh, replacement, or recovery consultant session is about to receive only `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, an accepted-state summary, a patch summary, or a narrow delta without the real baseline artifact body in that same outbound payload | set `VALIDATION_STATUS: blocked`, emit `BLOCKED_STATE: artifact-not-pasted`, replace the outbound request with a real baseline repaste in that same session, and do not count or send the narrowed prompt first | 1 |
| consultant response is missing any member of the consultant-shaped minimum (`consultant_verdict`, `strongest_finding`, `proposed_fix`) | set `CONSULTANT_QUALITY: failed` and retry once with the narrow consultant template | 1 |
| `CONSULTANT_QUALITY: failed` still holds after the one allowed retry | downgrade to `analysis-only`, keep the contiguous status block honest, and do not pretend a consultant-bearing success occurred | 0 additional |
| validation failed or blocked after a real patch | execute the `State Transition & Rollback Gate`, refresh continuity from the reverted artifact, and mark the patch attempt failed for that scope; do not continue the patch loop there unless a new materially different fix is proposed from the failure evidence | 1 |
| an OpenClaw-targeted skill, code artifact, workflow, runtime component, package-readiness claim, or publish-readiness claim is being optimized, validated, or described as OpenClaw-grounded without inspection of the relevant real local OpenClaw runtime code and instruction surfaces for that scope | set `VALIDATION_STATUS: blocked`, emit `BLOCKED_STATE: openclaw-runtime-not-grounded`, inspect the missing local OpenClaw runtime surfaces when available, or narrow the claim explicitly to `theoretical-provisional-unverified-against-local-OpenClaw`, then continue only from that honest narrowed state | 1 |
| a skill, code artifact, workflow, tool, runtime component, memory system, orchestrator, or program is being described as current-date-optimized, trend-aware, state-of-the-art, latest-practice-aligned, or materially improved against current external practice without live inspection of relevant public internet evidence even though an allowed internet-capable consultant/orchestrator is available and the task materially benefits from that check | set `VALIDATION_STATUS: blocked`, emit `BLOCKED_STATE: current-date-trend-not-grounded`, inspect the missing live public evidence when allowed, or narrow the claim explicitly to `offline-only-provisional-not-verified-against-current-public-trends`, then continue only from that honest narrowed state | 1 |
| runtime ambiguity is being resolved from a subordinate section or `references/` file instead of the `Runtime Core Lock` and inline artifact text | ignore the subordinate wording for runtime resolution, re-evaluate from the `Runtime Core Lock` and inline artifact text only, record `SYNC_DRIFT: subordinate-runtime-shadow` in the next `SYNC_POINT` or accepted-state summary, then synchronize the stale support surface | 1 |
| orchestrator response is still pending after a successful submit, with no explicit tool/runtime failure signal and no visible continuity break | keep waiting inside the same round/session; do not classify the round as failed, weak, degraded, or non-meaningful yet. Minimum wait floor after a confirmed successful submit is 60s for ordinary prompts and 120s for long/heavy prompts before lateness alone may contribute to degradation handling. After that floor, prefer one longer poll/wait on the same session before any recovery move. Late-but-valid answers count as normal round completion, not recovery evidence. | 1 wait-floor extension before any degradation judgment |
| session pollution, stale continuity, or context-length degradation is detected because the active orchestrator session is critiquing a pre-patch artifact state, repeating already-fixed findings, losing task identity, hallucinating against the visible same-topic chat history, carrying obvious nonsense against the visible accepted state, or the latest accepted `STATE_SNAPSHOT` does not match the active artifact | first try to resume the intended persistent same-topic session and verify continuity there; open a recovery session only if that intended session is unusable or has clearly degraded into nonsense, then repaste the latest accepted artifact and `RESUME_SNIPPET`, rebuild from the latest accepted `STATE_SNAPSHOT`, and verify continuity before continuing; do not trigger this branch from lateness alone before the orchestrator-response wait-floor rule above is satisfied. If that recovery session also degrades into nonsense, repeat the same same-orchestrator recovery shape instead of abandoning persistent-chat law | 1 per degraded chat |
| the current consultant/orchestrator launch path triggers approval cards or repeated authorization prompts for work that is otherwise allowed | do not claim the safeguard can be disabled and do not try to remove authorization globally; switch once to a launch path that stays inside the same safety boundary but avoids the prompt-triggering transport, preferably direct stdin or file redirection when the runtime supports it, then resume the same round/session and record the transport change honestly | 1 |
| a failure condition is not an exact match for any rule above | narrow scope explicitly or stop as blocked; do not improvise a multi-step recovery chain | 0 |

### Self-evolution lock
Activate the self-evolution lens when ANY of these are true:
- the artifact under review is `dual-thinking`
- the user asks `dual-thinking` to improve itself
- the artifact is a skill in the same native domain as `dual-thinking`
- the user asks for stronger self-review, meta-review, self-hardening, or self-rewrite
- the user asks how to make the skill more powerful for the purpose it was created for

When active:
- use outside-self reasoning as if the current artifact were written by someone else
- optimize for strength-for-purpose, not preservation-first comfort
- preserve real invariants, not familiar wording
- prefer the smallest patch that materially strengthens the skill
- treat praise as near-zero value unless it protects a distinctive strength from accidental removal
- reject commentary-only convergence when a real patch or explicit structural deferral is still required
- apply native-purpose maximization: optimize for skill review, rewrite, hardening, weak-model optimization, packaging, testing, and publish-readiness rather than continuity of authorship
- run the self-obsolescence test explicitly: ask where a stronger replacement would simplify, harden, compress, re-order, or delete current structure
- treat comfort, prior publication, prior validation, and familiarity as non-arguments unless they defend a real invariant
- do not accept `this is already strong` as a stopping reason by itself
- when `dual-thinking` reviews itself, improves itself, or improves a skill, code artifact, program, workflow, or runtime component inside OpenClaw, inspect the relevant local skill corpus and the relevant real local OpenClaw runtime surfaces, including code and instruction surfaces that govern how that artifact is actually loaded, routed, constrained, validated, packaged, or executed on that host, before convergence, structural deferral, or publish-readiness conclusions
- when an allowed internet-capable consultant/orchestrator is available and the task materially benefits from current-date external research, inspect the latest relevant public trend, architecture, implementation, benchmark, and maintainer evidence for the artifact's native domain on the current date, but preserve all binding local-only, privacy, hardware, runtime, and user-defined constraints while translating that evidence into the strongest compatible solution
- capability harvest is runtime-complete only if it proposes at least one evidenced reusable quality tied to a specific failure mode, validation gap, recovery seam, operator-risk seam, or publish-risk seam in the current artifact, or explicitly records that no evidenced transfer applies
- when local capability harvest is active, execute the compact validation defined in `## Local Capability Harvest Rule`; do not run verbose interrogation lists, but do not relax the minimum required round block or `VALIDATION_STATUS` visibility
- do not hallucinate harvested strengths, and do not treat decorative wording or project-specific noise as harvested capability
- keep unique downstream consequences in later sections only; do not redeclare this doctrine as parallel runtime law below the Reference Manual Boundary

### Current-date native-purpose maximization lock
When reviewing, rewriting, hardening, or creating any skill, code artifact, program, workflow, tool, or system artifact through Dual Thinking, do not optimize merely for incremental improvement of the current form. Optimize for the strongest realistically justified version of that artifact for its native purpose on the current creation or revision date.

Activation rule:
- this lock is binding by default whenever the routed task is `artifact-review`, `artifact-improvement`, `skill-review`, `skill-rewrite`, `skill-hardening`, or `skill-publish-readiness` and the artifact under review or change has a clear native mission
- it changes stance inside the routed task; it does not create a new public mode or a new runtime stage
- if the artifact's mission is still unclear, make the mission explicit or narrow scope before continuing; do not silently fall back to preservation-first review

Binding rules:
- treat the current artifact as a replaceable baseline, not as the target shape to preserve by default
- ask what a stronger current-date version of this artifact should look like if designed now for the same mission
- prefer current best-practice architecture, reliability patterns, operability patterns, validation discipline, maintainability patterns, and domain-appropriate performance and safety patterns when they materially strengthen the artifact
- do not preserve stale structure, weak defaults, legacy ceremony, or historically inherited limits unless they defend a real invariant, compatibility boundary, validated strength, or user-required constraint
- if the artifact belongs to a specific native domain such as memory, orchestration, networking, runtime safety, packaging, testing, or review, evaluate it against the strongest relevant current patterns for that domain rather than generic quality advice
- if the user asks to improve a named artifact with a clear mission, interpret the task as make it genuinely strong for that mission on the current date, not make it slightly cleaner while preserving its old ceiling
- trends are not authority by themselves; import only modern patterns that materially improve strength-for-purpose, reliability, recovery, clarity, maintainability, performance, safety, testability, or publish-readiness
- preserve real invariants, compatibility requirements, validated strengths, and user constraints, but do not treat age, familiarity, prior publication, prior praise, or prior validation as reasons to keep a weaker structure
- when multiple upgrade paths exist, prefer the smallest change that most increases present-day strength for the artifact's native purpose
- if the stronger present-day solution would require a structural change that the current line cannot absorb safely, record that explicitly as a structural deferral or next-line upgrade instead of silently settling for a weaker patch

Domain interpretation rule:
- memory skill such as `super-memori` -> optimize toward a genuinely stronger current memory system
- orchestrator -> optimize toward a genuinely stronger current orchestration system
- code, application, or runtime tool -> optimize toward a genuinely stronger current implementation for its mission

Stop-rule clarification:
- `already good`, `already published`, `already validated`, or `close enough to the existing form` are not sufficient stopping reasons by themselves
- completion requires either a real strengthening patch, or an explicit justified structural deferral when the stronger path cannot safely land in the current line

### Current-date Internet Trend Grounding Lock
When Dual Thinking reviews, rewrites, hardens, packages, validates, or creates any skill, code artifact, workflow, tool, runtime component, memory system, orchestrator, or program, and at least one allowed internet-capable consultant/orchestrator is available for that run, it must inspect the latest relevant public internet evidence for the artifact's native domain on the current date before concluding that the artifact is current-date-optimized, trend-aware, state-of-the-art, latest-practice-aligned, or genuinely strong relative to current external practice.

For in-scope current-date-sensitive work, this inspection has a minimum round-shape floor, not merely a generic evidence requirement. If the task is materially about current best practice, current comparative strength, current architectural direction, current competitive level, publish/release readiness against current external practice, or whether a named artifact is genuinely strong on the current date, then the first two consultant-bearing rounds must use internet-assisted review when an allowed internet-capable consultant/orchestrator is available. Round 1 must inspect live relevant public evidence and name the strongest current-date seam or missing strength in the real local artifact. Round 2 must challenge the applicability of round 1's external finding against the real local artifact, including truth boundaries, runtime limits, weak-model safety, operator constraints, and current accepted-state evidence. After round 2, later rounds do not need a repeated broad web scan unless a new materially disputed seam appears.

This lock operates only within already-binding user and artifact constraints. Internet trend inspection must refine the solution inside those constraints, not override them. If the artifact, user, or runtime requires local-only operation, no external APIs, no cloud dependencies, no remote runtime resources, no network dependency at runtime, or hardware-specific deployment boundaries, those constraints remain binding while the trend scan looks for the strongest compatible local implementation patterns.

Relevant current-date external evidence includes, as applicable to the task:
- current public technical articles, documentation, repositories, benchmarks, release notes, implementation guides, and maintainer guidance relevant to the artifact's native domain
- current public techniques, architectures, algorithms, storage patterns, retrieval patterns, compression patterns, inference patterns, runtime patterns, validation patterns, or safety patterns relevant to the requested scope
- current public evidence about what is materially stronger, faster, safer, lighter, more local, more hardware-compatible, more memory-efficient, or more reliable under the user's stated deployment constraints
- current public evidence that a hyped, generic, cloud-first, or externally dependent trend is incompatible with the user's constraints and therefore should be rejected rather than imported

Binding rules:
- When an allowed internet-capable consultant/orchestrator is available and the task materially benefits from current-date external trend awareness, inspect live public evidence before making strong latest-practice, state-of-the-art, or current-date optimization claims.
- For in-scope current-date-sensitive tasks, round 1 and round 2 consultant-bearing review must satisfy the minimum two-round internet-assisted floor described above; do not skip straight to local-only convergence while that floor remains unsatisfied.
- Round 1 internet-assisted review must answer both: what current external practices or trends are actually relevant here, and what strongest missing seam or strength gap they imply for the real artifact.
- Round 2 internet-assisted review must attack round 1's applicability to the real artifact and may reject, narrow, or redirect the external finding if it would break local truth, runtime constraints, safety, or operator honesty.
- After that minimum floor is satisfied, repeated broad internet scanning is optional and should happen only when a new materially disputed seam appears; do not turn this lock into ritual web-search churn for purely local bug, test, contract, or consistency work.
- If genuinely fresh live internet evidence visible in the current round materially contradicts an earlier-round external finding while the artifact under review is still materially the same, treat the fresh live check as evidence refresh rather than unlawful research drift or session inconsistency. Do not invoke this rule for stale session residue, repeated consultant memory, or unsupported restatements that do not actually present refreshed external evidence in the current round. Re-evaluate synthesis from the refreshed external evidence, and if the conflict matters, record that the earlier finding became stale instead of preserving it for continuity comfort alone.
- Do not treat offline prior knowledge, stale model memory, or generic architectural intuition as sufficient proof of current-date external alignment when live verification is available and relevant.
- Do not use internet trend scouting to override explicit local-only, privacy, hardware, latency, budget, safety, runtime, or user-defined constraints.
- If the artifact must stay local, use the internet only to discover the strongest compatible local methods, not to smuggle in cloud-first, hosted, or external-API solutions.
- When the user asks to improve a named artifact, search for advances specific to that artifact's native problem class, not just broad generic AI advice.
- Prefer evidence that matches the actual scope, hardware class, runtime constraints, deployment model, and operator requirements of the requested artifact.
- Reject trend cargo-culting. A fashionable approach is not authority unless it materially improves the artifact within the binding constraints.
- Before any current-date or latest-practice conclusion, record what external evidence categories or sources were actually inspected, or emit an explicit blocked or narrowed state naming what was not checked.
- That record must appear in visible round output as an explicitly labeled `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` entry inside `SYNTHESIS`, `SYNTHESIS_COMPACT`, `SYNC_POINT`, or an explicitly labeled accepted-state summary for the current decision surface; hidden reasoning or unlabeled narrative mention does not satisfy this lock.
- A round where this lock is active and the required visible `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` label is absent must set `VALIDATION_STATUS: blocked` and `BLOCKED_STATE: grounding-evidence-not-labeled`; the round is not passed.
- If live internet inspection is unavailable, disallowed, too weak, or too indirect for a grounded claim, narrow the claim honestly to offline-only, provisional, or not-verified-against-current-public-trends.
- No later section may downgrade this lock into advice, a soft preference, or a best-effort suggestion.

### Current-date Internet Trend Grounding Stability Lock
The Current-date Internet Trend Grounding Lock is stability-critical for skill engineering, code improvement, runtime design, and artifact hardening when live internet research is allowed and materially relevant. It may only be clarified or strengthened. It must not be weakened, softened, bypassed, narrowed, or removed without the user's explicit personal instruction. The round-1 / round-2 internet-assisted minimum floor for in-scope current-date-sensitive tasks is part of this stability-critical lock and may be clarified or strengthened but not relaxed into advice, best effort, or optional behavior. No convenience argument, token-saving argument, latency argument, summary-only argument, stale-memory argument, generic-best-practice argument, or ritual-avoidance argument is valid grounds for relaxing it. No later section may override this invariant. If any conflict appears, the stricter current-date-trend-grounding interpretation wins.

### Current-date Internet Trend Grounding Anti-Patterns
- Do not call an artifact current-date-optimized just because the text sounds modern.
- Do not rely on stale model knowledge alone when live internet verification is available and relevant.
- Do not skip the mandatory round-1 / round-2 internet-assisted floor for in-scope current-date-sensitive tasks just because the artifact already looks strong.
- Do not turn this lock into ritual repeated web search for purely local bug, test, contract, or consistency work after the mandatory floor has already been satisfied.
- Do not import cloud-first, hosted, or external-API designs into a local-only artifact.
- Do not use generic AI trends as proof of fit for the user's hardware, runtime, locality, privacy, or deployment constraints.
- Do not weaken this rule without the user's explicit personal instruction.

### OpenClaw Runtime Grounding Lock
When Dual Thinking reviews, rewrites, hardens, packages, validates, or creates any skill, code artifact, workflow, tool, runtime component, or publish-ready artifact intended to run inside OpenClaw or depend materially on OpenClaw behavior, it must inspect the relevant real local OpenClaw runtime surfaces before concluding that the artifact is OpenClaw-optimized, OpenClaw-grounded, runtime-ready, package-ready, publish-ready, or genuinely strong for OpenClaw rather than only strong in theory.

Relevant OpenClaw runtime surfaces include, as applicable to the task:
- the local OpenClaw code that governs skill discovery, skill loading, routing, invocation, toolcommand execution, sandboxing, approval boundaries, packaging, validation, or publication for the target artifact path
- the local OpenClaw system, developer, operator, or shipped instruction surfaces that constrain how skills are supposed to behave on that host
- the local skill directory conventions, packaging surfaces, validator surfaces, config schemas, and commandtool policy surfaces relevant to the artifact
- any local runtime outputs, validator outputs, or host-scoped evidence needed to distinguish real OpenClaw behavior from generic agent theory

Binding rules:
- Do not optimize an OpenClaw-targeted artifact from generic agent best practice alone when OpenClaw-specific behavior is materially relevant.
- Do not claim OpenClaw optimization from skill quality alone.
- Do not treat theoretical compatibility, generic shell assumptions, guessed skill-loading behavior, or abstract agent-design patterns as proof of OpenClaw fit.
- Inspect the real local OpenClaw runtime surfaces that matter for the requested scope before convergence, structural deferral, packaging, publish-readiness, or OpenClaw-specific strength claims.
- If the local OpenClaw runtime surfaces are unavailable, inaccessible, incomplete, stale, or too indirect to justify a grounded claim, narrow the claim honestly to theoretical, provisional, unverified-against-local-OpenClaw, or generic-best-practice-only.
- When the artifact can still be improved generically without the missing OpenClaw runtime evidence, improvements may continue, but every OpenClaw-specific claim must remain explicitly limited by the missing-surface state.
- When real local OpenClaw behavior conflicts with generic best practice, prefer the real OpenClaw behavior for OpenClaw-targeted optimization unless the user explicitly asks for portability-first design instead.
- Before any OpenClaw-specific convergence or readiness conclusion, record which OpenClaw runtime surfaces were actually inspected, or emit an explicit blocked or narrowed state that names the missing surfaces.
- That record must appear in visible round output as an explicitly labeled `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` entry inside `SYNTHESIS`, `SYNTHESIS_COMPACT`, `SYNC_POINT`, or an explicitly labeled accepted-state summary for the current decision surface; hidden reasoning or unlabeled narrative mention does not satisfy this lock.
- A round where this lock is active and the required visible `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` label is absent must set `VALIDATION_STATUS: blocked` and `BLOCKED_STATE: grounding-evidence-not-labeled`; the round is not passed.
- Inspecting only the local skill corpus is not enough when the task depends on how OpenClaw itself loads, routes, constrains, validates, or executes that artifact.
- No later section may downgrade this lock into advice, a soft preference, or a best-effort suggestion.

### OpenClaw Runtime Grounding Stability Lock
The OpenClaw Runtime Grounding Lock is stability-critical for any OpenClaw-targeted artifact path. It may only be clarified or strengthened. It must not be weakened, softened, bypassed, narrowed, or removed without the user's explicit personal instruction. No convenience argument, token-saving argument, summary-only argument, prior-publication argument, prior-validation argument, or generic best-practice argument is valid grounds for relaxing it. No later section may override this invariant. If any conflict appears, the stricter OpenClaw-grounding interpretation wins.

### OpenClaw Runtime Grounding Anti-Patterns
- Do not call a skill OpenClaw-optimized just because the skill text is strong in isolation.
- Do not assume OpenClaw skill-loading, routing, command execution, sandbox, approval, packaging, or validator behavior without inspecting the real local OpenClaw runtime surfaces.
- Do not treat generic agent-design theory as proof of OpenClaw fit.
- Do not weaken this rule without the user's explicit personal instruction.

## Local Capability Harvest Rule
This is a hard strengthening rule for native-domain self-improvement and OpenClaw artifact review.
When local capability harvest is active, inspect the relevant local skill corpus and pull forward only evidenced reusable qualities that can harden the current artifact against a specific failure mode, validation gap, recovery seam, operator-risk seam, or publish-risk seam.
A harvest step is valid only if it does one of these:
- proposes at least one concrete strengthening patch tied to one such specific seam
- records an explicit `no evidenced transfer` conclusion for the current seam in visible round output, typically in `SYNTHESIS`, `SYNTHESIS_COMPACT`, or a clearly labeled accepted-state summary
Do not treat decorative wording, branding language, or project-specific noise as harvested capability.
Do not hallucinate a quality that was not evidenced by the local corpus.
Actual artifact rewrites still require the normal patch, validation, rollback, and publish gates.
Read `references/harvest-doctrine.md` when syncing capability-harvest rationale, examples, or preservation policy. Purpose: non-runtime doctrine and examples.

## Capability Harvest Preservation Lock
Already-identified evidenced reusable strengths and harvested capabilities are additive-by-default.
They may be clarified, tightened, or better formulated, but they must not be silently removed, weakened, forgotten, or replaced by a weaker form.
If one is intentionally removed or weakened, that change must be recorded explicitly as a conscious decision, not smuggled in as wording cleanup.
Only the user's explicit personal instruction may authorize weakening or removal of an already-identified harvested strength.
If any conflict appears, the stronger preserved harvested-capability interpretation wins until an explicit decision records otherwise.

## Fundamental Context Isolation Rule
This is a hard invariant.
No round logic, role logic, consultant logic, session-reuse logic, payload-shaping logic, comparison logic, evidence logic, or synthesis logic overrides it.

- External models are blind by default.
- They only see the text explicitly sent in the current request.
- If the transport reuses the same visible consultant chat or session, the consultant can see only the text explicitly present in that same visible chat or session. A new chat does not inherit old chat context unless it is explicitly resent. Shorter payloads, narrower prompts, or follow-up convenience do not create implicit visibility.
- No consultant sees arbiter context unless the arbiter pastes it.
- No consultant sees another consultant's context unless it is explicitly pasted.
- External models do not see local paths, local files, file contents that were not pasted, arbiter reasoning, hidden notes, draft comparisons, other-model prompts, other-model answers, other-model context, other-model reasoning, prior-round system context, local command output, local validation output, or repository state unless that exact content is explicitly pasted as text.
- A local file path is not file access.
- If content was not pasted, the external model did not see it.
- Every consultant request must be self-contained.
- If a consultant needs code, logs, requirements, constraints, acceptance criteria, or file content, paste the exact needed text. Do not rely on filenames, paths, summaries, or implied context.
- If the arbiter is not sure the consultant has enough context, fail closed: resend the missing context in text or say explicitly that the context was not provided. Never fill the gap with an assumption of shared visibility.

## Context Isolation Stability Lock
The Fundamental Context Isolation Rule is a stability-critical invariant.
It must not be weakened, softened, bypassed, shortened in meaning, or reinterpreted into a shared-visibility model.
Convenience, brevity, payload reduction, round compression, token savings, prompt simplification, or easier consultant reuse are not valid reasons to relax it.
It may only be clarified or strengthened.
If real runtime evidence shows that correction is needed, it must be corrected only toward stricter correctness and better isolation discipline.
No later section may override, dilute, or silently narrow this invariant.
If any conflict appears, the stricter consultant-isolation interpretation wins.

## Persistent Orchestrator Session Inviolability Lock
This is a stability-critical invariant for consultant-bearing continuity.
In `api` and especially in `multi`, the default law is persistent same-topic consultant chat reuse.
For a given same-topic line, each external consultant or orchestrator must remain in its own persistent visible chat or session across the full round series.
Starting a fresh chat merely because a new round began is forbidden.
Convenience, payload reduction, token savings, cleaner transcripts, stylistic preference, or the agent's desire for a "fresh start" are not valid reasons to abandon the persistent same-topic chat.

In `multi`, this rule is strict:
- DeepSeek keeps one persistent same-topic chat for the line
- Qwen keeps one persistent same-topic chat for the line
- later rounds must continue inside those same per-orchestrator chats
- switching to a newly created chat is invalid unless the recovery conditions below are actually met

The only ordinary recovery reason to replace a persistent consultant chat is consultant degradation inside that very chat.
For this skill, consultant degradation means the active consultant has started producing obvious nonsense, losing the visible task identity, contradicting the visibly accepted artifact state without grounded evidence, repeating already-fixed findings as if they were still unresolved, or otherwise "carrying nonsense" against the visible same-topic history.

When that degradation condition appears, the recovery law is narrow and mandatory:
1. do not switch to an arbitrary fresh pattern
2. do not silently abandon the persistent-chat scheme
3. create exactly one replacement chat for that same orchestrator
4. mark `CHAT_CONTINUITY: recovery`
5. repaste the latest accepted artifact, the latest `RESUME_SNIPPET`, and any exact accepted-state deltas needed for honest review
6. continue trying inside that replacement chat for the same orchestrator

If the replacement chat for that same orchestrator also degrades into nonsense, repeat the same recovery shape again: create a new replacement chat for that same orchestrator, repaste the latest accepted state, and continue honestly.
Do not use consultant nonsense as an excuse to downgrade the session law into free chat rotation.
Do not treat arbitrary new-chat creation as normal alternation behavior.
Do not switch recovery strategy merely because the agent feels the old sequence is inconvenient.

This rule may be violated only under true force-majeure conditions that make honest continuation in that persistent-chat lineage impossible under the Runtime Core Lock.
Outside true force majeure, violation is forbidden.
The rule itself may be weakened or rewritten only by the user's explicit personal instruction.
It may otherwise only be clarified or strengthened, never softened.
If any conflict appears, the stricter persistent-session interpretation wins.

## User-Declared Round Commitment Lock
If the user explicitly declares a cycle-count, round-count, or total round plan before execution, that declared plan becomes binding runtime commitment.
A user-declared round plan is binding.
It must run to completion.
The run must continue until the full declared cycle/round plan is completed.
Early stop is forbidden merely because the current artifact looks good, convergence seems strong, the agent agrees with itself, the consultant agrees, the patch looks sufficient, or the closure checklist would otherwise allow stopping.
Convenience, brevity, token savings, convergence comfort, impatience, repetition fatigue, or stylistic confidence are not valid reasons to shorten a user-declared round plan.
This commitment may be interrupted only by true force-majeure conditions or by the user's explicit personal instruction.
No ordinary closure rule may terminate a declared round plan before that plan is complete.
If the user declared more than one cycle before execution, no user-facing progress reply may be emitted between cycles; continue straight into the next cycle and reply only after all declared cycles complete, unless a lawful force-majeure condition applies or the user explicitly instructs otherwise.
If a consultant round, validation step, or other checkpointed execution step completes successfully and `NEXT_ACTION` is already known while the declared plan remains unfinished, continue immediately into that `NEXT_ACTION`; do not wait for a fresh user ping unless the user explicitly requested a pause or a lawful force-majeure condition applies.
This inter-cycle no-reply rule and this no-idle-after-completion rule are stability-critical and may be changed only by the user's explicit personal instruction.
This rule augments current stop logic only; it does not weaken or bypass the Runtime Core Lock, the State Transition & Rollback Gate, the Recovery Decision Tree, the Fundamental Context Isolation Rule, the Context Isolation Stability Lock, validation honesty, blocked-state honesty, or any lawful recovery requirement.
No later section may override this invariant.

### Allowed force-majeure interruption only
Allowed interruption reasons are limited to:
- explicit personal user stop or rewrite of the round plan
- hard runtime failure that prevents honest continuation
- blocking artifact-not-pasted state that cannot be resolved inside the allowed recovery path
- safety boundary or authorization boundary that prevents lawful continuation
- unrecoverable continuity loss where the accepted state cannot be reconstructed honestly
- validation or execution state that makes further rounds dishonest or impossible under the Runtime Core Lock
- any already-defined hard-blocked state that the Runtime Core Lock treats as non-continuable

For a user-declared multi-cycle plan, an inter-cycle user-facing progress reply is itself an interruption unless the user explicitly asked for it or a lawful force-majeure condition requires it.
For a user-declared unfinished plan, post-step idleness after a successful completed round, completed validation step, or completed tool/process result is itself an interruption unless the user explicitly asked for a pause or a lawful force-majeure condition requires it.
Closure logic may confirm completion only after the declared plan is actually complete; it may not pre-empt that plan.

Normal convergence is not force majeure.
`already enough` is not force majeure.
agreement is not force majeure.
good patch quality is not force majeure.
repeated findings are not force majeure by themselves.

## Round Commitment Stability Lock
The User-Declared Round Commitment Lock is stability-critical.
It may only be clarified or strengthened.
It must not be changed without the user's explicit personal instruction.
It must not be weakened, softened, bypassed, or converted back into optional stop behavior.
No convenience argument is valid grounds for relaxing it.
No later section may override this invariant.
If any conflict appears, the stricter round-commitment interpretation wins.

## Round Commitment Anti-Patterns
- Do not stop early just because the artifact already looks strong.
- Do not stop early because self and consultant agree.
- Do not treat closure satisfaction as permission to ignore a user-declared round plan.
- Do not reinterpret a user-declared plan as a soft target.
- Do not reduce cycles or rounds for convenience, brevity, token savings, or repetition fatigue.
- Do not silently collapse a multi-cycle plan into a shorter run.
- Do not emit an inter-cycle user-facing progress reply during a user-declared multi-cycle plan unless the user explicitly asked for it or lawful force majeure applies.
- Do not sit idle after a successful completed round, validation step, or tool/process result when `NEXT_ACTION` is already known and the declared plan is still unfinished.
- Do not claim force majeure when the real reason is ordinary convergence.
- Do not weaken this rule without the user's explicit personal instruction.

## Context Isolation Anti-Patterns
- Do not send full context to consultant A and a reduced fragment to consultant B while assuming B can infer or access A's context.
- Do not reference local file paths as if external models can open them.
- Do not assume a new chat inherits earlier context.
- Do not create a new consultant chat on a later round merely because it feels cleaner, safer, shorter, or easier.
- Do not use consultant degradation as an excuse to abandon the persistent same-orchestrator session law; recover by recreating that same orchestrator's chat and continuing honestly.
- Do not assume the arbiter's internal reasoning, draft notes, hidden comparisons, or unstated accepted state are visible to consultants.
- Do not assume one consultant can see another consultant's answer, prompt, or context unless it is explicitly pasted.
- Do not assume the consultant knows file contents because the arbiter knows them.
- Do not assume prior rounds, prior system context, or prior validation results are visible unless they were explicitly resent in text to that same consultant.
- Do not use excerpts in a fresh or recovery consultant session unless the baseline artifact is visibly repasted in that same session first.
- Do not count a consultant round whose visible baseline was not proven in that same session.
- Do not weaken or shorten the context-isolation rule just because repeated context passing feels expensive, redundant, or inconvenient.

## Baseline Visibility Fail-Closed Lock
This is a stability-critical hard rule for consultant-bearing review.
In any fresh consultant chat, replacement chat, recovery chat, or other consultant session where visible baseline continuity is not already proven inside that same session, excerpt use is forbidden until the baseline artifact is visibly repasted there.

Binding rules:
- Fresh consultant session means no excerpt rights by default.
- Recovery consultant session means no excerpt rights by default.
- Replacement consultant session means no excerpt rights by default.
- In those sessions, the arbiter must repaste the real artifact as fully as practical, or a genuinely sufficient canonical excerpt bundle that fully covers the exact claims under review, before any narrowing is allowed.
- Excerpt use becomes lawful only after that baseline artifact payload is visibly present in that same consultant session.
- `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, patch summaries, and intent-to-repaste notes are continuity aids only; they do not satisfy baseline visibility and they do not create excerpt rights by themselves.
- If baseline visibility in that same session is uncertain, treat it as not proven.
- If baseline visibility in that same session is not proven, the round is invalid and must not be counted toward any user-declared quota, round total, convergence claim, or release-readiness claim.
- After an `artifact not pasted`, `not visible`, or equivalent consultant response, the next step must be a real baseline repaste in that same session or a new recovery session; do not answer with another summary, pointer, thin excerpt, or accepted-state digest.
- Paraphrase, wrapper text, intent summary, path mention, assumed continuity, or continuity-only summary artifacts do not satisfy this lock.
- A later section may clarify or strengthen this lock, but it may not weaken, soften, bypass, or reinterpret it into best-effort behavior.

## Baseline Visibility Stability Lock
The Baseline Visibility Fail-Closed Lock is stability-critical.
It may only be clarified or strengthened.
It must not be weakened, softened, bypassed, narrowed, or removed without the user's explicit personal instruction.
No convenience argument, payload-size argument, latency argument, token-saving argument, transport assumption, session-memory assumption, or "the consultant probably saw it" argument is valid grounds for relaxing it.
If any conflict appears, the stricter baseline-visibility interpretation wins.

## Before Sending Any Consultant Request
Before any external consultant call, check all:
- Is this request self-contained?
- Did I include the exact code, text, log, requirement, constraint, and acceptance-criteria excerpts needed for the answer?
- Am I relying on invisible arbiter knowledge?
- Am I assuming this model saw another model's context?
- Am I assuming this new chat still has the old chat context?
- If the answer requires file content, did I paste the relevant content instead of only naming the file or path?
- If the answer depends on prior rounds, did I explicitly resend the needed prior-round text to this same consultant?
- Am I silently relaxing the context-isolation invariant for convenience, brevity, token savings, or payload reduction?
- If this is a fresh, replacement, or recovery consultant session, did I prove visible baseline repaste in this same session before using any excerpt?
- Am I mistaking `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, an accepted-state summary, or a patch summary for proof that the baseline artifact was repasted in the outbound payload?
- If anything required is missing, stop and resend the missing context in text or acknowledge that it was not provided.

## Reference Manual Boundary
Everything below this boundary is subordinate to the Runtime Core Lock and the Fundamental Context Isolation Rule.
Use later sections, references, and examples as support material, checklists, validator surfaces, and detailed decompositions.
If a lower section feels broader, more legalistic, or more detailed than the Runtime Core Lock, do not let it silently become the real execution law.
Self-review stance, local capability harvest, harvested-capability preservation, current-date native-purpose maximization, native-purpose targets, and patch sizing are fully governed by the `Self-evolution lock`, `Local Capability Harvest Rule`, `Capability Harvest Preservation Lock`, and `Current-date native-purpose maximization lock` above; no parallel doctrine applies below this boundary.

## Deterministic Router

Evaluate router conditions in order. The first matching semantic condition sets `MODE`.

If the user explicitly asked for alternating orchestrators before round 1, set `ORCHESTRATOR_MODE: multi`, keep one persistent session per orchestrator, and continue routing to set `MODE`. Do not silently create a fresh consultant chat on later rounds just because a new round started.
If the user explicitly asked for findings only, set `MODE: analysis-only` and do not patch.
If the topic is a skill or skill-adjacent artifact and the requested outcome is a concrete rewrite, set `MODE: skill-rewrite`.
If the topic is a skill or skill-adjacent artifact and the requested outcome is runtime, safety, weak-model, or operability tightening, set `MODE: skill-hardening`.
If the topic is a skill or skill-adjacent artifact and the requested outcome is packaging, release gating, sharing, or publication, set `MODE: skill-publish-readiness`.
If the topic is a skill or skill-adjacent artifact and the requested outcome is weak-model clarity specifically, set `MODE: weak-model-optimization`.
If the topic is a skill or skill-adjacent artifact, set `MODE: skill-review`.
If the user wants an artifact changed, set `MODE: artifact-improvement`.
If the user wants an artifact assessed, set `MODE: artifact-review`.
Otherwise set `MODE: general-decision-review`.

If multiple intents overlap, keep the first-match semantic mode already encountered. Do not blend modes.
The self-evolution lens does not create a fourth public stage or a new public mode. It changes stance inside the existing three-step architecture.

## Runtime Contract
The enforceable execution rules are defined by the `Runtime Core Lock`, the terminal Minimum Required Round Block rule, the contiguous status-block rule, and the mode/closing-tail semantics already defined inline above.
This section now stays as a pointer only; duplicated enums, paths, and block definitions must not become a second runtime source of truth or a fallback runtime authority.

### When not to use dual-thinking
Do not use the method when all are true:
- the action is reversible in under 1 hour
- the risk is low
- the requested change is small
- no real trade-off or uncertainty remains

If all are true, act directly instead of opening the full dual-thinking loop.
If the request is trivial and no real critique is needed, skip the method.
Do not spend review rounds on formatting-only churn unless the user explicitly asked for wording polish.

#### Extended consultation structure
Use the full form when the runtime can support it.

```text
SELF_POSITION:
- initial_verdict: <short verdict>
- strongest_points: <1-3 bullets>
- likely_weaknesses: <1-3 bullets>
- smallest_strong_fix: <one concrete fix>
- confidence: <low|medium|high>
- what_could_change_my_mind: <one short condition>

CONSULTANT_POSITION:
- consultant_verdict: <short verdict>
- strongest_finding: <one strongest finding>
- weakest_or_vague_finding: <one weak point or `none`>
- proposed_fix: <smallest strong fix from consultant>
- confidence: <low|medium|high|unknown>

SYNTHESIS:
- relation: <aligned|partially-aligned|divergent>
- keep_from_self: <what stays from self position>
- keep_from_consultant: <what stays from consultant>
- reject: <what is rejected and why>
- final_decision: <take|keep|merge|reject|defer>
- final_next_action: <one clear next step>
```

Rules:
- `SELF_POSITION` is a real pre-consultant position, not a decorative summary after the fact.
- Build `SELF_POSITION` from the actually loaded artifact.
- In `api` and `multi`, do not ask the consultant before producing `SELF_POSITION`.
- After a consultant response, extract `CONSULTANT_POSITION` before deciding.
- In `api` and `multi`, do not jump from consultant response directly to final decision.
- `DECISION` and `NEXT_ACTION` must be grounded in `SYNTHESIS` whenever a consultant-bearing round occurred.
- Stance for this phase is governed exclusively by the applicable lock in `## Runtime Core Lock` above.

#### Compact consultation structure
Use this only for weak-model constrained rounds.

```text
SELF_POSITION_COMPACT:
- verdict: <...>
- weakness: <...>
- fix: <...>

CONSULTANT_POSITION_COMPACT:
- consultant_verdict: <...>
- strongest_finding: <...>
- proposed_fix: <...>

SYNTHESIS_COMPACT:
- relation: <aligned|partial|divergent>
- decision: <...>
- next_action: <...>
```

Rules:
- compact form is allowed for weak-model constrained rounds
- compact form is not permission to skip the three-step logic
- in `api` and `multi`, do not omit `SELF_POSITION` entirely
- in `api` and `multi`, do not omit `SYNTHESIS` entirely
- compact consultant output must remain consultant-position-shaped by default unless the round has explicitly moved to a synthesis compaction step
- if consultant input is still required but unavailable after retries, narrow to `analysis-only` or mark the round invalid instead of pretending the structure existed
- stance for this phase is governed exclusively by the applicable lock in `## Runtime Core Lock` above

## Consultation status requirements by mode

```text
Mode-specific status requirements:
- `local`:
  - `SELF_POSITION_STATUS` must be `present` or `compact`
  - `CONSULTANT_POSITION_STATUS` must be `not-applicable`
  - `SYNTHESIS_STATUS` must be `present` or `compact`

- `api`:
  - `SELF_POSITION_STATUS` must be `present` or `compact`
  - `CONSULTANT_POSITION_STATUS` must be `present` or `compact`
  - `SYNTHESIS_STATUS` must be `present` or `compact`

- `multi`:
  - on every consultant-bearing round:
    - `SELF_POSITION_STATUS` must be `present` or `compact`
    - `CONSULTANT_POSITION_STATUS` must be `present` or `compact`
    - `SYNTHESIS_STATUS` must be `present` or `compact`

- `analysis-only`:
  - compact or partial consultation structure is allowed only if the narrowed scope explicitly justifies it
  - do not pretend a full consultant-bearing structure happened when it did not
```

Validation consequences:
- If `ORCHESTRATOR_MODE: local`, then `CONSULTANT_POSITION_STATUS: not-applicable` is the only valid consultant status.
- If `ORCHESTRATOR_MODE: api` or `multi`, then `CONSULTANT_POSITION_STATUS: not-applicable` is invalid for a consultant-bearing round.
- In consultant-bearing modes, `SELF_POSITION_STATUS`, `CONSULTANT_POSITION_STATUS`, and `SYNTHESIS_STATUS` are mandatory round-state enums, not optional extended niceties.
- If a consultant-bearing round omits any required consultation status enum, validation must fail.
- If a consultant-bearing round lacks `SYNTHESIS_STATUS`, validation must fail unless the round was explicitly narrowed out of consultant-bearing execution.

Rules:
- A round that violates the required status pattern for its mode cannot be treated as fully valid unless the narrowed mode explicitly permits partial structure.
- synthesis stance for this phase is governed exclusively by the applicable lock in `## Runtime Core Lock` above.

## Consultant prompt shaping

```text
For `api` and `multi` modes, the consultant prompt must include:
1. the real artifact
2. the current task or requested scope
3. the current `SELF_POSITION`
4. an explicit instruction to agree, refine, or challenge the current position
5. a request for consultant-position output, not immediate final synthesis unless explicitly narrowed to synthesis
```

Rules:
- Do not ask the consultant to produce the final round decision by default.
- The consultant provides input to synthesis; the main agent remains responsible for final synthesis and final decision.
- The consultant-visible prompt must contain the real artifact text itself, not just a path, filename, repository pointer, `FILE:` label, shell command, unresolved placeholder, or my own summary of unseen material.
- Literal command substitutions such as `$(cat path/to/file)` count as unresolved placeholders when they appear in the transmitted prompt body.
- If a prompt only references where the artifact lives instead of embedding the text itself, treat that round as `artifact not pasted`.
- If the claim under review depends on local checks, test output, validation results, command results, or code not already visible in that same consultant session, paste those exact results in text before asking for critique.
- consultant stance for this phase is governed exclusively by the applicable lock in `## Runtime Core Lock` above.

### Consultant Blindness Clarification

The Fundamental Context Isolation Rule applies here without exception.

In `api` and `multi`, external consultants are blind by default.
They only see the text explicitly sent in the current request.
If the transport reuses the same visible consultant chat or session, the consultant can see only the text explicitly present in that same visible chat or session. A new chat does not inherit old chat context unless it is explicitly resent.
No consultant sees arbiter context unless the arbiter pastes it.
No consultant sees another consultant's context unless it is explicitly pasted.
The consultant cannot see local files, local paths, repository state, project code, hidden main-agent context, unstated accepted state, local command output, local validation results, screenshots, non-pasted sections of the artifact, hidden notes, or other-model prompts or answers unless that exact information was explicitly transmitted in text in the visible consultant prompt/session.
A local file path is not file access.
If content was not pasted, the external model did not see it.

Use these formulas:
- `not pasted = not visible`
- `not visible = not reviewed`
- `local to me ≠ visible to consultant`
- `summarized by me ≠ verified by consultant`
- `path or filename ≠ artifact text`

Do not claim consultant review of sections, files, checks, code, logs, or state that were not actually pasted.
If the consultant's finding depends on non-pasted material, treat that finding as ungrounded until the relevant text is pasted and re-reviewed.
Do not assume cross-consultant visibility in `multi`; if round N depends on text seen only by the other consultant, repaste that text into the active consultant's own session before asking for review.

### Baseline artifact requirement

For the first consultant-bearing round on a new skill topic, do not use summary-only review.

Paste the artifact as fully as practical, or paste a large enough canonical excerpt bundle that really covers the issue.
If the round asks the consultant to judge a specific section, invariant, failure mode, code path, test result, or local verification outcome, the prompt must also paste the exact relevant text for that claim in visible form.

Later narrower rounds are valid only after baseline context was already transmitted in that same consultant-visible conversation and only when the omitted material is truly unchanged and already visible in that same consultant's own session. If that session is fresh, replacement, or recovery, narrowing is forbidden until visible baseline repaste is proven there under the Baseline Visibility Fail-Closed Lock.

Clarification:
- first consultant-bearing round on a new skill topic should use a baseline artifact payload, not a thin summary
- later narrower prompts are valid only after that baseline context already exists in the same visible consultant session
- fresh/recovery/replacement consultant sessions have no excerpt rights until that visible baseline is repasted and therefore proven in that same session
- `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, and patch summaries do not substitute for that baseline repaste in fresh/recovery/replacement sessions
- if you switch consultants, do not assume the new consultant inherits the other consultant's pasted context; repaste what the new consultant needs
- do not assume the consultant can infer unseen artifact sections from the skill name, file path, repository, prior hidden state, or your private local work
- if you want the consultant to reason about code, checks, logs, tests, or validation, paste that material in text
- do not feed consultants chopped fragments when the claim under review needs broader surrounding context to stay grounded

Example consultant prompt shape:

```text
I already formed an internal position on this artifact.

SELF_POSITION:
<block>

Critique the real artifact directly.
Do one of:
- agree and strengthen
- refine
- challenge with stronger reasoning

Return only:
- consultant_verdict
- strongest_finding
- weakest_or_vague_finding
- proposed_fix
- confidence
```

When the self-evolution trigger is active, shape the consultant prompt like this instead:

```text
I already formed an internal position on this artifact.

SELF_POSITION:
<block>

Review this artifact as if you were designing the stronger successor that should replace it.
Challenge the current form.
Prefer forceful critique over praise.
Identify where the current artifact is trapped in a local maximum.
Name what should be removed, tightened, or redesigned.
Return the smallest strong fix, not admiration.

Return only:
- consultant_verdict
- strongest_finding
- weakest_or_vague_finding
- proposed_fix
- confidence
```

Do not ask for the final round `DECISION` in this prompt unless the flow has explicitly moved into synthesis compaction.

#### Local mode rule
If `ORCHESTRATOR_MODE: local`, set `ORCHESTRATOR: local`.
The agent is the only consultant in local mode.
`SELF_POSITION` is mandatory in local mode.
There is no `CONSULTANT_POSITION` in local mode.
Do not output `CONSULTANT_QUALITY` in local mode.
Do not use model names in local mode.
Do not imitate an external consultant call in local mode.
Treat local mode as self-consultation plus self-synthesis plus decision.

#### API mode rule
If `ORCHESTRATOR_MODE: api`, the required order is:
1. `SELF_POSITION`
2. external `CONSULTANT_POSITION`
3. `SYNTHESIS`
4. patch or next action

Round 2+ for the same topic must reuse the same consultant chat or session by default so the consultant can see only the prior rounds and payload text already given in that same chat.
Open a fresh consultant chat only if the intended same-topic chat cannot be safely reused because continuity is broken, the chat is polluted, or the consultant is clearly degrading under context load and producing nonsense against the visible prior round history.
If such degradation occurs, the new chat is a recovery continuation of that same consultant line, not a free reset of the session law; repaste the latest accepted state and continue there.
Outside true force majeure, no other reason is lawful.
Do not reorder this into consultant-first review.

#### Multi-orchestrator alternation contract
If `ORCHESTRATOR_MODE: multi`, alternate by round and keep one persistent session per orchestrator for the topic.
Do not let both orchestrators free-run on the same round in parallel unless the caller explicitly asks for that.
The default continuity rule is strict: each orchestrator must stay in its own same-topic chat across the full round series so that consultant can see only the prior rounds and payload text already given to it in that same chat.
Each of those chats is isolated from the other orchestrator's chat. Reuse inside consultant A's own chat preserves A-context only; reuse inside consultant B's own chat preserves B-context only.
Starting a fresh consultant chat on round 2+ is invalid by default and must not be treated as normal alternation behavior.
Open a replacement chat only if the intended persistent chat is unusable because continuity is broken, the session is polluted, or the consultant is clearly degrading under context length and starts repeating already-fixed findings, losing task identity, or producing nonsense against the visible accepted state.
If replacement is required, mark `CHAT_CONTINUITY: recovery`, repaste the latest accepted artifact and `RESUME_SNIPPET`, and continue only after the replacement chat has enough context to review the current state honestly.
If that replacement chat also degrades into nonsense, create another replacement chat for that same orchestrator, repaste the latest accepted state again, and continue there. Recovery repetition does not dissolve the persistent per-orchestrator chat law.
Outside true force majeure, no other basis may be used to violate this continuity rule.
The required sequence for a multi round is:
1. load the latest accepted artifact state
2. produce one `SELF_POSITION` for that artifact state
3. resume the intended persistent orchestrator session for that round only by making the needed continuity text visible there again; do not assume hidden transport memory and do not open a fresh chat unless the recovery rule above applies
4. paste the latest accepted artifact, not a stale pre-patch copy
5. include the latest `RESUME_SNIPPET` and any other accepted patch context or prior-round text that is still needed for grounded review in that visible session
6. obtain critique from exactly one orchestrator for that round
7. extract `CONSULTANT_POSITION`
8. produce `SYNTHESIS`
9. emit a `SYNC_POINT` summary with accepted findings, rejected findings, and the current next action
10. patch accepted fixes before the next round when required
11. emit or refresh `STATE_SNAPSHOT` before switching orchestrators

`STATE_SNAPSHOT` must minimally preserve:
- current round number
- active topic slug
- routed `MODE`
- per-orchestrator session keys
- latest accepted artifact version or hash
- latest accepted findings summary
- latest `SELF_POSITION` summary or hash reference
- latest consultant-side summary for recovery fidelity
- `support_surfaces_synchronized` when one or more subordinate support surfaces were synchronized in the accepted state; otherwise omit it or set it to `none`
- `deferred_patch_context` when the latest rollback or deferred patch outcome must remain exact across handoff; otherwise set it to `none`
- latest `RESUME_SNIPPET`
- `LAST_CONSULTANT` when the next round needs explicit consultant-side continuity context; otherwise omit it or set it to `na`

Use `LAST_CONSULTANT` only as a continuity hint.
It does not override the alternation invariant in `multi` mode.
It helps recovery and handoff clarity; it does not choose the next orchestrator by itself.

`RESUME_SNIPPET` must explicitly list any material continuity deltas that change the resuming session's starting assumptions, such as active synchronized support surfaces, deferred patch outcomes, or overridden next actions. If no such deltas apply, it may remain a compact state summary.

Use this concrete shape when you need to serialize it:

```text
STATE_SNAPSHOT:
  round: <N>
  topic: <slug>
  mode: <mode>
  session_a: <key>
  session_b: <key>
  artifact_hash: <hash-or-version>
  self_position: <compact summary>
  consultant_summary: <compact summary>
  accepted_findings: <compact summary>
  support_surfaces_synchronized: <surface-slug-list-or-none>
  deferred_patch_context: <diff-slug-or-none>
  last_consultant: <session-key|local|na>
  resume_snippet: |
    <latest RESUME_SNIPPET>
```

After each consultant round in `multi` mode, emit this handoff shape before switching orchestrators:

```text
SYNC_POINT:
  round: <N>
  accepted: |
    - <finding slug>
  rejected: |
    - <finding slug> (reason: <short reason>)
  support_surfaces_synchronized: |
    - <surface slug> (omit when none)
  next_action: <one clear next step>
```

If a multi-round recovery is required, restore from the latest accepted `STATE_SNAPSHOT`, not from raw memory of prior chat turns.
The alternation invariant is simple: round 1 uses orchestrator A, round 2 uses orchestrator B, later rounds keep alternating while reusing the same per-orchestrator sessions.
Consultant context should accumulate inside those same persistent chats only to the extent that the transport actually preserves visible chat history there; if the needed history is not visibly present, repaste the required context before asking for review.
Do not discard that continuity and restart round-specific fresh chats unless the explicit recovery rule applies. Token savings, payload reduction, convenience, cleaner transcripts, or aesthetic preference are not recovery reasons.
Do not treat consultant nonsense as permission to roam across arbitrary fresh chats; the lawful response is recovery by recreating the same orchestrator's chat lineage and continuing from the latest accepted state.

Blind-session clarification:
- each orchestrator session is independently blind except for what was actually pasted into that specific session
- do not assume orchestrator B knows what was only pasted to orchestrator A
- do not assume orchestrator A knows what was only pasted to orchestrator B
- do not assume hidden main-agent context transfers automatically
- do not assume a consultant can read your local files, project tree, codebase, shell history, validator output, or test results unless you pasted them into that same visible session
- when switching orchestrators, repaste the latest accepted artifact or the relevant accepted excerpt needed for grounded review
- if the next round depends on text, code, checks, or decisions that were visible only in the other consultant's chat, repaste them into the active consultant's own chat before asking for review
- if the next round depends on a local check you performed, repaste the exact check result in text before asking the consultant to rely on it
- if the current launch transport keeps triggering approval cards for otherwise allowed work, do not try to disable safeguards globally; switch to a less approval-prone transport such as direct stdin or file redirection when supported, keep the same safety boundary, and continue honestly from the accepted state

### Synthesis honesty clarification

`SYNTHESIS` may only attribute consultant coverage to text actually visible to that consultant.

Allowed:
- `consultant reviewed the provided excerpt`
- `consultant responded to the supplied artifact section`
- `consultant reviewed the pasted check output`

Disallowed:
- `consultant reviewed the skill` when the full skill was not pasted
- `consultant reviewed the updated artifact` when the updated artifact was not pasted
- `consultant reviewed the code` when only a filename or path was given
- `consultant considered my validation/tests/logs` when those results were not pasted into the visible prompt/session

#### Failure and round-meaningfulness authority
For runtime failure handling, blocked states, retry caps, and non-meaningful-round recovery, use the authoritative `Recovery Decision Tree` in `## Runtime Core Lock`.
This subordinate section no longer carries primary runtime law for the current execution line.
Preserve only the boundary rule here: a long wait after a successful consultant submit is not by itself evidence of a weak or failed round. Minimum wait floor before lateness alone can contribute to failure/degradation handling is 60s for ordinary prompts and 120s for long/heavy prompts, and one longer same-session wait/poll should be preferred before recovery. `SELF_POSITION` alone is not enough in `api` or `multi` when consultant input was required and available, and `SYNTHESIS` must still exist.

#### Round-Limit & Stop Precedence
Resolve stop behavior in this order:
1. If the user explicitly declared a cycle-count, round-count, or total round plan before execution, that declared plan is binding runtime commitment and must run to completion unless a force-majeure condition from the `User-Declared Round Commitment Lock` applies or the user explicitly rewrites the plan.
2. If that declared plan includes more than one cycle, do not emit a user-facing progress reply between cycles unless the user explicitly asked for one or a lawful force-majeure condition requires it.
3. If a consultant round, validation step, or other checkpointed execution step completes successfully and `NEXT_ACTION` is already known while the declared plan remains unfinished, continue immediately into that `NEXT_ACTION`; do not wait for a fresh user message unless the user explicitly requested a pause or a lawful force-majeure condition applies.
4. If the user explicitly authorized a higher round count for the current flow before round 1, that explicit limit overrides the default `MAX_ROUNDS` note.
5. If a round produces `CONTINUATION_SIGNAL: stop` while a user-declared round plan remains unfinished, override the signal, continue to the next lawful step, and do not stop unless a force-majeure condition applies. A normal stop signal is invalid while a declared round plan remains unfinished.
6. If the resolved round limit has been reached, force `CONTINUATION_SIGNAL: stop` for the next decision point unless the user explicitly authorized more rounds or already declared a larger binding round plan before execution.
7. If a round is non-meaningful, recover or narrow scope first and do not treat that attempt as convergence by itself.
8. Otherwise continue according to the normal convergence and failure rules.

#### Skill-task closure checklist
For skill topics, stop only if all are true for the asked scope. This checklist is subordinate to `User-Declared Round Commitment Lock` and cannot lawfully terminate an unfinished declared round plan:
- `CONTINUATION_SIGNAL: stop`
- I also agree
- no accepted fix remains unpatched
- no runtime-critical ambiguity remains for the asked scope
- no must-have docs remain missing for the asked scope
- no must-have tests remain missing for the asked scope
- no unresolved blocker remains for the asked scope
- if the user declared a binding round plan before execution, the full declared plan has actually been completed or a force-majeure condition applies under the `User-Declared Round Commitment Lock`
- if the declared plan included more than one cycle, no inter-cycle user-facing progress reply was emitted unless the user explicitly requested it or a lawful force-majeure condition applied
- if the declared plan remained unfinished and `NEXT_ACTION` was already known, no post-step idle pause occurred after a successful completed round, validation step, or tool/process result unless the user explicitly requested a pause or a lawful force-majeure condition applied

## Required Modes
Keep these modes available and route with the Deterministic Router. Read `references/modes.md` when you need the full mode table and mode-specific entry rules. Purpose: map task types.

## Skill Review Checklist

If the topic is a skill, always check the 12 review angles defined in `references/skill-review-mode.md`.
Stance for this phase is governed exclusively by the applicable lock in `## Runtime Core Lock` above.
Use `references/self-evolution-lens.md` and other review references only as supporting checklists, not as a second doctrine source.

When the self-evolution lens or OpenClaw artifact-improvement path is active, apply the compact harvest validation defined in `## Local Capability Harvest Rule`; do not restate harvest questions here, and do not treat that compactness as permission to relax the minimum required round block or `VALIDATION_STATUS` visibility.

If a skill fix is accepted, the next round must include a real patch in the real artifact, not only a suggestion list.
If self and consultant both detect stagnation under the self-evolution lens, escalate toward a real patch or an explicit structural deferral instead of settling for commentary alone.
- Stop behavior, force-majeure limits, and declared round plans are governed exclusively by `User-Declared Round Commitment Lock` and `Round-Limit & Stop Precedence`; do not re-evaluate them through checklist questions.

## Patch State

Emit patch state when patch work exists, an accepted fix is still pending, or a patch blocker must be logged.
If no patch work exists, `PATCH_STATUS: none` is enough and `PATCH_MANIFEST` may be omitted.

```text
APPLY: <done|deferred|not-needed>
PATCH_MANIFEST:
- target: <file or section>
  change: <one-line description>
  status: <proposed|applied|re-reviewed|rejected>
  version_bump: <none|patch|minor|major>
```

## Round Output Contract

Every round ends with the inline Minimum Required Round Block and contiguous status order defined in this document, emitted exactly once after synthesis and decision. Reference files may mirror that structure for sync and validation, but they do not override it.
For weak models, emit the fully populated minimum required round block exactly once at the end of the round. Add extended fields only when they help.
`VALIDATION_STATUS` is mandatory in the minimum round block and must resolve before `PATCH_STATUS` is emitted as accepted state. For `PATCH_STATUS: none`, emit an explicit resolved value such as `passed` or `not-applicable` rather than omitting the field.
If an external validator schema conflicts with the inline round-block structure required by this document, the inline requirement wins and the external file must be flagged for maintenance.

## Publish Scope and Gate

Publish, release, and package gates are required only in `skill-publish-readiness` or when the user explicitly asked for shipping, distribution, packaging, or readiness.
If publish scope is not requested, `PUBLISH_STATUS` may remain `Draft`, `Reviewed`, `Hardened`, or `Deferred` without adding extra packaging runtime obligations.
If `VALIDATION_STATUS: failed` or `blocked`, block packaging and publishing.

For `skill-publish-readiness`:
- `VALIDATION_STATUS: passed` is required before `PUBLISH_STATUS: Packaged` or `PUBLISH_STATUS: Published`; the full atomic sequencing and accepted-state rules remain governed exclusively by `State Transition & Rollback Gate`.
- `TEST_STATUS` and `VERIFICATION_EVIDENCE` become conditionally mandatory round-block fields for the current publish gate
- heading version alignment and detailed package-content / ClawHub packaging checks belong to subordinate support surfaces (`PACKAGING_CHECKLIST.md`, synced reference artifacts, and release evidence), not to a second inline runtime law

## Weak-Model Shortcut

If you cannot safely manage the full review flow, use this fallback.
Treat the current path as weak-model constrained if either of these is true:
- upfront constraints or the first consultant attempt already show that the round cannot reliably maintain structured output or session/mode stability
- the consultant repeats generic praise after the real artifact was pasted inline
- the consultant cannot keep the mode, session, or next-action state stable across one round

Shortcut contract:
- preserve the routed `MODE`
- paste the real artifact inline in enough detail for the exact claim under review
- produce `SELF_POSITION_COMPACT`
- if the round is still consultant-bearing, request `CONSULTANT_POSITION_COMPACT`
- produce `SYNTHESIS_COMPACT`
- follow the round-block emission discipline defined by the `Runtime Core Lock` and `Round Output Contract`

Authority note:
- consultant-shaped minimum, retry caps, downgrade-to-`analysis-only`, `CONSULTANT_POSITION_STATUS: omitted-invalid`, and failure routing are governed exclusively by the Runtime Core Lock and the Recovery Decision Tree
- narrowing defaults to consultant-position output first; decision-style narrowing is synthesis-only
- shortcut stance for this phase is governed exclusively by the applicable lock in `## Runtime Core Lock` above

### Narrow consultant template — normal consultant-bearing rounds
```text
Focus strictly on <section>.
Name exactly 1 structural weakness.
Give the smallest strong fix.
Return only:
- consultant_verdict
- strongest_finding
- weakest_or_vague_finding
- proposed_fix
- confidence
No praise. No preamble.
```

### Narrow synthesis fallback — only when the caller explicitly requests decision-ready compaction
```text
Focus strictly on <section>.
Given the current SELF_POSITION and the consultant critique, output only:
- relation
- decision
- next_action
No praise. No preamble.
```

## Execution

The executable sequence is already defined by the inline Runtime Core Lock, the round block contract, the mode semantics, and the shared closing tail rules above.
This section intentionally stays short to avoid reintroducing mirrored runtime law.

Execution trace rule:
- route first
- preserve round context
- load the real artifact inline
- produce `SELF_POSITION`
- obtain exactly one consultant position when the mode is consultant-bearing
- produce `SYNTHESIS`
- validate
- apply accepted fixes to the artifact; advance accepted state only after validation passes and the accepted state can advance honestly
- emit the fully populated round block exactly once with resolved validation and patch state
- continue or stop

Mode note:
- `local` = self + synthesis only
- `api` = self -> one consultant -> synthesis
- `multi` = alternate one orchestrator per round, refresh accepted continuity state before handoff, and keep one persistent session per orchestrator for the topic

Closing-tail note:
After the mode-specific core produces the decision state, apply the shared closing tail exactly once. Do not duplicate emit/patch/validate logic in parallel prose paths.

## Maintenance & Release Gates

- `CONSULTANT_QUALITY: mixed` means the response contained at least one structurally sound actionable finding, but also included vague, hallucinated, or only partially aligned points. Keep the good parts, reject the bad parts, and do not retry automatically if the actionable path is already clear.
- `analysis-only` is a valid operating mode, not a failure state.
- In `local` mode, do not output `CONSULTANT_QUALITY`.
- `MAX_ROUNDS`: default `5` unless the user explicitly wants more and did not already declare a binding larger round plan before execution.
- In `multi` mode, alternate one orchestrator per round and keep the per-orchestrator sessions stable for the topic.
- For ClawHub publish-readiness, `.clawhubignore` must exist and must not exclude required package artifacts.
- `CONSULTANT_QUALITY: weak` handling is governed by the Runtime Core Lock, the Recovery Decision Tree, and the Weak-Model Shortcut above; do not reintroduce a parallel retry policy here.
- Packaging and publishing preconditions are governed exclusively by `Publish Scope and Gate` and `State Transition & Rollback Gate`; do not restate publish rules here, to prevent parallel-law drift.
- Publish only if the user asked for distribution and the publish gate has been satisfied.

Reference files remain required sync and package surfaces for this skill, but they are subordinate to the inline runtime contract. Use them to keep validators, scenarios, examples, packaging, and release evidence aligned with the inline authority; do not let them become a second executable runtime path, a fallback execution path, or a competing source of runtime truth.

## Artifact Governance
Governance and release-policy detail is non-runtime and lives in `GOVERNANCE.md`.
Use that file for freeze policy, release criteria, validation-state taxonomy, backlog discipline, done-enough heuristics, and line-state / lineage labels.
Do not encode candidate/release lineage labels in the runtime header of `SKILL.md`.
Inline runtime law still wins for execution behavior.
If the current line is frozen, structural changes must still route to the next candidate line unless a required scenario test proves a defect in the current reference-release line.

## Required scenario tests
Required scenario ownership lives in `references/reference-scenarios.md` and the freeze / release-policy gates in `GOVERNANCE.md`.
Those validation surfaces define which scenario failures justify bugfixes, candidate-line work, release blocking, or structural deferral.
They do not add a second executable runtime path on top of the inline `Runtime Core Lock`.
A structural change is justified only if one of those required scenarios fails or a newly required scenario with clear operational value is explicitly adopted through the reference/governance surfaces.

## Reference validation status
Reference-line maturity states and backlog/governance policy are defined in `GOVERNANCE.md`.
Keep `PUBLISH_STATUS` separate from reference-line maturity.

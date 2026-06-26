# Changelog

## 8.5.24 - 2026-04-25
- Hardened both grounding locks with an inline fail-closed consequence: if the required visible `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` label is absent while the lock is active, the round must emit `VALIDATION_STATUS: blocked` and `BLOCKED_STATE: grounding-evidence-not-labeled` and is not passed.
- Kept the frozen-line patch small by reusing existing validation/blocked-state machinery instead of adding new round schema or retry procedure.

## 8.5.23 - 2026-04-25
- Tightened both grounding locks so inspected external/runtime evidence or blocked/narrowed grounding state must appear in visible round output as explicitly labeled `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` rather than being satisfiable by hidden reasoning or unlabeled narrative.
- Kept the frozen-line patch budget honest by closing the grounding-accountability gap without adding a new mandatory minimum round-block field.
- Advanced the visible candidate line to `8.5.23` after the accepted grounding-evidence visibility clarification.

## 8.5.22 - 2026-04-25
- Hardened fresh/recovery/replacement-session baseline law so continuity-only artifacts (`STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, patch summaries) are explicitly forbidden as substitutes for real baseline repaste.
- Added a fail-closed Recovery Decision Tree branch that blocks a narrowed outbound consultant request when a fresh/recovery/replacement session would otherwise receive continuity-only context without the real baseline artifact body.
- Tightened the pre-send checklist and baseline-visibility wording so invalid recovery prompts are stopped before send rather than being rationalized after the fact.

## 8.5.21 - 2026-04-14
- Canonicalized Recovery Decision Tree state/block key names to the same underscore-separated forms used by the live runtime contract (`VALIDATION_STATUS`, `BLOCKED_STATE`, `CONSULTANT_QUALITY`, `CONSULTANT_POSITION_STATUS`, `SYNC_POINT`, `STATE_SNAPSHOT`, `RESUME_SNIPPET`, `SYNC_DRIFT`).
- Synced subordinate runtime/failure/test surfaces to that recovery-key canonicalization so weak-model parsing and recovery routing no longer rely on mixed naming styles.
- Corrected `references/reference-freeze.md` to the truthful active `v8.5.21` reference-candidate line and synchronized remaining active-line version-honesty surfaces.

## 8.5.20 - 2026-04-14
- Added a non-weakenable `Baseline Visibility Fail-Closed Lock`: fresh, replacement, and recovery consultant sessions now have no excerpt rights until visible baseline repaste is proven in that same session.
- Invalid consultant rounds caused by missing visible baseline must not be counted toward quotas, convergence, or release-readiness claims.
- Synced runtime/reference/failure/test surfaces to that fail-closed ratchet.

## 8.5.19 - 2026-04-14
- Corrected the visible `SKILL.md` heading version from stale `v8.5.14` to the truthful active `v8.5.19` line so the published artifact stays version-honest.
- Synced active support/evidence surfaces to the publish-honesty heading fix.

## 8.5.18 - 2026-04-14
- Added a guardrail to the current-date evidence-refresh rule: it now applies only when genuinely fresh live external evidence is visible in the current round, not when a consultant is merely repeating stale session residue or unsupported memory.
- Synced failure-handling and active support/evidence surfaces to that guardrail.

## 8.5.17 - 2026-04-14
- Added an explicit current-date evidence-refresh rule to the inline `Current-date Internet Trend Grounding Lock`: if a fresh live internet check later contradicts an earlier-round external finding while the artifact is still materially the same, the newer live check governs for synthesis instead of being treated as unlawful research drift.
- Synced failure-handling and active support/evidence surfaces to the new evidence-refresh rule.
- Corrected active line metadata to the live `v8.5.17` candidate line, including the stale `references/runtime-contract.md` version note.

## 8.5.16 - 2026-04-14
- Added an explicit orchestrator late-answer minimum wait-floor to the inline Recovery Decision Tree so successful submits are not misclassified as weak/degraded/failed merely because the reply arrives later than expected.
- Bound lateness-only handling to a concrete floor: wait at least 60s for ordinary prompts and 120s for long/heavy prompts before lateness alone may contribute to degradation handling, and prefer one longer same-session wait/poll before recovery.
- Clarified that late-but-valid orchestrator answers count as normal round completion rather than retroactive evidence that the round was weak or failed.
- Synced subordinate failure-handling and reference-test-log surfaces to the new wait-floor rule.

## 8.5.15 - 2026-04-14
- Strengthened the inline `Current-date Internet Trend Grounding Lock` with a ratchet-rule minimum floor for in-scope current-date-sensitive tasks.
- Bound round 1 and round 2 consultant-bearing review to internet-assisted inspection when an allowed internet-capable consultant/orchestrator is available and the task is materially about current best practice, current comparative strength, current architectural direction, or publish/release readiness against current external practice.
- Made the two-round floor explicit: round 1 must name the strongest current-date seam from live external evidence against the real artifact; round 2 must challenge the applicability of that external finding against local truth boundaries, runtime limits, weak-model safety, and operator constraints.
- Locked that two-round floor as stability-critical so future revisions may clarify or strengthen it but may not weaken it without the user's explicit personal instruction.
- Added explicit anti-pattern coverage so the lock cannot collapse into either stale-memory-only review or ritual repeated web search after the minimum floor is already satisfied.
- Synced package/evidence/reference/test surfaces to the new `v8.5.15` line.

## 8.5.14 - 2026-04-14
- Published the current-date trend-grounding support-surface sync as the next version after the already-published `8.5.13` line.
- Kept the inline runtime authority unchanged while synchronizing subordinate governance, checklist, validator, evidence, and test surfaces to the live current-date trend-grounding hard-lock family.
- Added lower-stack coverage for `BLOCKEDSTATE: current-date-trend-not-grounded`, the matching recovery branch, and the self-evolution live-public-evidence requirement.

## 8.5.13 - 2026-04-14
- Added an inline OpenClaw Runtime Grounding Lock, its Stability Lock, and matching anti-patterns above the Reference Manual Boundary so OpenClaw-targeted work cannot honestly claim OpenClaw optimization without inspecting the real local OpenClaw runtime surfaces.
- Extended the Recovery Decision Tree with the `openclaw-runtime-not-grounded` blocked state and strengthened the self-evolution rule so OpenClaw self/workflow reviews require both local skill-corpus inspection and relevant real local OpenClaw runtime surface inspection.
- Added the `Current-date Internet Trend Grounding Lock`, `Current-date Internet Trend Grounding Stability Lock`, and `Current-date Internet Trend Grounding Anti-Patterns` inline above the Reference Manual Boundary.
- Extended the Recovery Decision Tree with `BLOCKEDSTATE: current-date-trend-not-grounded` and strengthened self-evolution so materially relevant current-date external claims require live public trend, architecture, implementation, benchmark, and maintainer evidence when an allowed internet-capable consultant/orchestrator is available.
- Synced governance, validator, checklist, evidence, reference, and test surfaces so the lower stack supports the live inline current-date trend-grounding hard-lock family instead of shadowing it.

## 8.5.12 - 2026-04-13
- Strengthened the persistent orchestrator session law so violating the same-topic per-orchestrator chat scheme is lawful only under true force majeure.
- Made explicit that consultant degradation/nonsense permits only same-orchestrator recovery-chat continuation, not free rotation across arbitrary fresh chats.
- Locked the rule so it may otherwise only be clarified or strengthened, and may be weakened only by the user's explicit personal instruction.

## 8.5.11 - 2026-04-13
- Continued the fresh 8-round alternating self-rerun on top of the `v8.5.10` candidate line.
- Clarified rollback refresh so reverting to the last passed artifact must also refresh `support_surfaces_synchronized` and related support-surface tracking fields from the reverted accepted state.
- Kept the current line publish-honest by advancing the visible candidate version only after accepted, locally revalidated patches.

## 8.5.10 - 2026-04-13
- Fresh full 8-round alternating self-rerun on top of the published `v8.5.9` baseline using AI Orchestrator and Qwen Orchestrator.
- Added an explicit removal/clearing rule for `support_surfaces_synchronized` during accepted-state transitions so disappearance is handled as honestly as appearance.
- Bound the artifact's visible version/release label to accepted patched state when `PATCH_MANIFEST.version_bump` is not `none`, unless a justified deferral is recorded.
- Remaining rounds continue as a falsification pass against the strengthened `v8.5.10` candidate line; publish depends on the final validation and publish gate.

## 8.5.9 - 2026-04-13
- Fresh full 8-round alternating self-rerun on top of the published `v8.5.8` baseline using AI Orchestrator and Qwen Orchestrator, with two honest Qwen stale-session recovery events before convergence.
- Added `Fresh-rerun support-surface honesty gate` so stale subordinate release/promotion/freeze/verification surfaces are demoted during a fresh rerun until the new line revalidates and resynchronizes them.
- Clarified the stale-to-current-support transition for subordinate support surfaces after explicit revalidation/resynchronization.
- Made synchronized support surfaces explicit continuity state across `SYNC_POINT`, `STATE_SNAPSHOT`, and their equality contract, closing handoff/restart drift.
- Added `RESUME_SNIPPET` generation rules so material continuity deltas must survive restart-oriented recovery summaries.
- Final later rounds converged honestly: no materially justified seam remained beyond cosmetic example-format normalization.

## 8.5.8 - 2026-04-13
- Fresh rerun intentionally paused after the first 3 accepted, validated rounds by explicit user instruction to publish now and postpone the rest.
- Round 1 made stop-signal handling under unfinished user-declared plans active and fail-closed: override the signal and continue unless force majeure applies.
- Round 2 added explicit `deferred_patch_context` to `STATE_SNAPSHOT` for exact rollback continuity across orchestrator handoff.
- Round 3 made subordinate-runtime-shadow recovery require explicit stale support-surface synchronization as a discrete action.

## 8.5.7 - 2026-04-13
- Micro-pass polish only; no architecture rewrite.
- Added `Capability Harvest Preservation Lock` immediately after `Local Capability Harvest Rule`.
- Tightened single-runtime-authority wording so reference, validator, and packaging surfaces cannot read as fallback runtime authority or competing runtime truth.
- Tightened declared-round-vs-closure wording and fail-closed consultant-isolation wording without changing runtime architecture.

## 8.5.6 - 2026-04-13
- Fresh 8-round alternating self-rerun completed using AI Orchestrator and Qwen Orchestrator.
- Accepted a round-1 clarification that compact harvest validation never relaxes the minimum required round block or `VALIDATION_STATUS` visibility.
- Accepted a round-3 governance clarification that records `v8.5.6` as an active working candidate during rerun without falsely claiming release state.
- Accepted a round-7 packaging-checklist correction replacing stale `v8.4.9` lineage text with the truthful frozen `v8.5.2` prior baseline.
- Final release sync updated version/evidence surfaces for the actual `v8.5.6` release after the full rerun and validation pack.

## 8.5.5 - 2026-04-13
- Fresh rerun from the published `v8.5.4` line accepted multiple frozen-line contradiction removals and execution-hardening clarifications before release.
- Added `User-Declared Round Commitment Lock`, `Round Commitment Stability Lock`, and `Round Commitment Anti-Patterns` so user-declared multi-round or multi-cycle plans are binding runtime law.
- Added a hard no-intercycle-reply rule for user-declared multi-cycle plans and a hard no-idle-after-completed-step rule when `NEXT_ACTION` is already known and the declared plan remains unfinished.
- Moved `VALIDATION_STATUS` into the minimum required round block and aligned `Round Output Contract` so validation/patch-state sequencing cannot drift for weak models.
- Synced runtime/reference/validator surfaces and added required scenarios for user-declared round commitment, no inter-cycle reply, and no idle after completed step.

## 8.5.4 - 2026-04-13
- Tightened the `Round Commitment Stability Lock` wording by removing one redundant sentence while keeping the stronger prohibition line unchanged.
- No runtime architecture change; this is a text cleanup only.

## 8.5.3 - 2026-04-13
- Fresh 12-round alternating exact-text self-rerun on top of the published `v8.5.2` baseline (2 full cycles of 6 rounds) using AI Orchestrator and Qwen Orchestrator, including one honest Qwen session-recovery event.
- Clarified `Execution trace rule` so artifact patch application is separated cleanly from accepted-state advancement, aligning the short execution summary with the atomic `State Transition & Rollback Gate`.
- Removed redundant standalone publish-precondition bullets from `Maintenance & Release Gates` and replaced them with a strict pointer to the authoritative `Publish Scope and Gate` and `State Transition & Rollback Gate` sections.
- Full second-cycle falsification failed to surface any further justified patch: after the two accepted clarifications, all later meaningful rounds converged on `no material seam remains` for the frozen line.

## 8.5.2 - 2026-04-13
- Fresh 6-round alternating exact-text rerun on top of the published `v8.5.1` baseline, with one honest stale-session Qwen rejection plus fresh-session recovery.
- Removed duplicate round-block-emission authority from `Weak-Model Shortcut` so that fallback flow now defers cleanly to `Runtime Core Lock` and `Round Output Contract`.
- Made the first consultant-bearing round baseline artifact requirement unconditional, removing the old subjective qualifier from `Baseline artifact requirement`.
- Clarified `Publish Scope and Gate` so `VALIDATION_STATUS: passed` is explicitly subordinate to the full atomic `State Transition & Rollback Gate` sequence.
- Reached convergence after the three accepted clarification patches; late passes confirmed no material seam remained in the exact current text.

## 8.5.1 - 2026-04-12
- Fresh post-release 6-round alternating rerun on top of the published `v8.5.0` baseline, plus one honest Qwen recovery round for a stale repeated seam.
- Compressed inline required-scenario ownership into a short pointer to `references/reference-scenarios.md` and `GOVERNANCE.md`, eliminating a second inline quasi-runtime doctrine block.
- Aligned the `## Execution` trace with the atomic validation gate so validation resolves before accepted patch application and before final round-block emission.
- Clarified multi-orchestrator continuity so persistent session reuse never implies hidden memory; required continuity now depends on visible repaste when needed.
- Removed vestigial `DRY_RUN` from `Patch State` so the runtime surface matches the current atomic apply/rollback model.

## 8.5.0 - 2026-04-12
- Compressed local capability harvest from a sprawling runtime doctrine into a tight runtime-verifiable rule tied to specific failure, validation, recovery, operator-risk, or publish-risk seams.
- Removed capability-harvest selection, preservation, and anti-pattern mega-sections from the main runtime contract so they no longer compete with `Runtime Core Lock` as parallel doctrine.
- Added `references/harvest-doctrine.md` as the non-runtime home for capability-harvest rationale, examples, and preservation guidance.
- Tightened `Self-evolution lock` and `Reference Manual Boundary` to keep capability harvest binding but subordinate, with lower cognitive load for weak models and consultant rounds.

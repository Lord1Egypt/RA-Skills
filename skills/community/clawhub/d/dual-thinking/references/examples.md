# Examples
#tags: skills review

## Example 1: initial activation for a skill rewrite
User request:
- `Rewrite this skill so weak models can execute it without stalling.`

Expected first-round state:
- `MODE: skill-rewrite`
- `SKILL_CLASS: workflow`
- `ORCHESTRATOR_MODE: api`
- `SESSION: dt-skill-name-yyyymmdd-api`
- produce `SELF_POSITION` before the first consultant request

## Example 2: weak-model shortcut
User request:
- `Just do a quick structural audit of this skill.`

Expected shortcut path:
- use the shortcut when the agent cannot safely manage the full review flow
- emit `ROUTE_COMPLETE`
- emit `SELF_POSITION_READY`
- if still in `api` or `multi`, emit `CONSULTANT_POSITION_READY`
- emit the full minimum round block first
- emit compact consultation blocks instead of skipping them
- keep flow control on `CONTINUATION_SIGNAL` plus the shared convergence rules instead of forcing a visible termination marker
- later recovery can start from the emitted `RESUME_SNIPPET` and latest accepted `STATE_SNAPSHOT`
- include `LAST_CONSULTANT` when it materially helps recovery or the next orchestrator handoff

## Example 3: same topic same chat
User request:
- `Continue reviewing the same skill.`

Expected behavior:
- round 2+ reuses the same chat or session for that topic
- emit `CHAT_CONTINUITY: reused`
- do not start a fresh chat unless continuity is broken, the session is polluted, or the consultant has clearly degraded under context load and can no longer use the visible same-topic chat honestly

## Example 4: alternating multi-orchestrator
User request:
- `Use Qwen and DeepSeek alternately for 6 rounds on this skill.`

Expected behavior:
- `ORCHESTRATOR_MODE: multi`
- `MODE:` stays the semantic task mode that was routed for the topic, such as `skill-review`, `skill-hardening`, or `skill-publish-readiness`
- Round 1 uses orchestrator A in its own persistent chat
- Round 2 uses orchestrator B in its own persistent chat
- later rounds return to the same per-orchestrator chats so each consultant accumulates its own prior rounds in one same-topic chat
- each consultant-bearing round starts from one fresh `SELF_POSITION` for the latest accepted artifact state
- the consultant prompt includes the artifact, current task, and current `SELF_POSITION`
- after each round, emit a `SYNC_POINT` summary and refresh the `STATE_SNAPSHOT`
- carry `LAST_CONSULTANT` in the handoff state when consultant-side continuity matters for the next round
- every accepted fix is patched before the next round
- open a replacement consultant chat only as recovery, never as the default round-to-round behavior

## Example 5: consultant prompt shaped from self-position
Use this structure in `api` and `multi` when the round asks an external consultant to agree, refine, or challenge.

```text
I already formed an internal position on this artifact.

SELF_POSITION:
<block>

Now critique the real artifact directly.
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

Rules:
- include the real artifact
- include the current task
- include the agent's current `SELF_POSITION`
- explicitly invite agreement, refinement, or challenge
- ask for consultant-position output by default, not the final round decision
- do not use path-only references, `FILE:` labels without body text, shell snippets, or literal placeholders like `$(cat ...)` instead of the actual artifact text

## Example 6: patch-bearing round
- emit `PATCH_STATUS: applied`
- patch the real artifact
- emit `APPLY: done`
- emit `PATCH_MANIFEST`
- include `version_bump` when runtime behavior changed

## Example 7: publish-readiness close
- run both validators
- run `test_round_flow.sh`
- run `test_reference_alignment.sh`
- ensure the current round block includes `TEST_STATUS: verified`
- ensure the current round block includes `VERIFICATION_EVIDENCE` with the executed commands and observed success signals
- package the skill only after the publish gate is satisfied
- set `PUBLISH_STATUS` to `Packaged` or `Published`
- if a blocker remains, set `PUBLISH_STATUS: Deferred`

## Example 8: local mode
- `ORCHESTRATOR_MODE: local`
- `ORCHESTRATOR: local`
- `SELF_POSITION_STATUS: present` or `compact`
- `CONSULTANT_POSITION_STATUS: not-applicable`
- `SYNTHESIS_STATUS: present` or `compact`
- `CONSULTANT_QUALITY` is omitted
- no model name is shown
- no external consultant call is implied
- local mode means self-consultation plus self-synthesis plus decision

## Example 9: consultant prompt shaping contract
- in `api` and `multi`, the consultant prompt includes the real artifact, current scope, and explicit `SELF_POSITION`
- the consultant is told to agree, refine, or challenge
- the consultant returns consultant-position fields by default
- final decision remains with synthesis by the main agent

## Example 10: bad first-round prompt with thin summary

```text
Please review this skill.
It is mostly about runtime contract quality and consultant blindness.
I think the issue is that the consultant may over-assume context.
Critique it.

[invalid for exact artifact review: thin summary only, no substantial artifact payload]
```

## Example 11: correct first-round prompt with substantial artifact payload

```text
You are reviewing a skill artifact.

Current scope:
- consultant blindness
- exact runtime contract wording
- multi-session artifact continuity
- synthesis honesty

Here is the real artifact text relevant to this review:

SKILL HEADER:
<pasted text>

RUNTIME CONTRACT SECTION:
<pasted text>

MULTI MODE SECTION:
<pasted text>

ROUND / SYNTHESIS SECTION:
<pasted text>

SELF_POSITION:
<pasted text>

Return only:
- consultant_verdict
- strongest_finding
- weakest_or_vague_finding
- proposed_fix
- confidence
```

Why this is correct:
- the consultant sees the actual artifact text
- the scope is explicit
- the self-position is explicit
- the round is grounded in pasted text rather than summary-only review

## Example 12: correct later-round narrowed prompt after baseline

```text
You already reviewed the baseline artifact for this topic in this same session.

Current narrowed scope:
- synthesis honesty wording for non-pasted sections

Latest accepted excerpt:
<pasted excerpt>

Delta since last accepted state:
<pasted changed wording>

RESUME_SNIPPET:
<pasted snippet>

SELF_POSITION:
<pasted text>

Critique only this updated excerpt.
Return only:
- consultant_verdict
- strongest_finding
- weakest_or_vague_finding
- proposed_fix
- confidence
```

Why this is correct:
- the narrowed round happens after baseline context already exists
- the consultant sees the exact updated excerpt
- the narrowed prompt still carries the current active state

## Example 13: self-review of dual-thinking with the self-evolution lens
User request:
- `Upgrade dual-thinking so it becomes harder to outperform in its own native domain.`

Expected behavior:
- structural classification occurs first
- if the current line is frozen and the change is structural, fork the next candidate line instead of mutating the frozen release line silently
- `SELF_POSITION` adopts an outside-self stance
- consultant prompt asks for stronger-successor critique instead of polite review
- `SYNTHESIS` decides from strength-for-purpose rather than loyalty-to-current-form
- accepted outcome is a real patch or an explicit justified structural deferral

## Example 14: challenge-heavy consultant prompt under self-evolution
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

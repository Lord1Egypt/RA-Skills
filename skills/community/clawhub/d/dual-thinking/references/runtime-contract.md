# Runtime Contract
#tags: skills review

Version note: aligned with the live Dual Thinking v8.5.24 reference-candidate line after the grounding-evidence fail-closed consequence hardening pass on top of the grounding-evidence visibility line.

## External Required Output
Keep these rules short and machine-checkable.

### Enum blocks
Use these values exactly.
- `MODE`: `general-decision-review` | `artifact-review` | `artifact-improvement` | `skill-review` | `skill-rewrite` | `skill-hardening` | `skill-publish-readiness` | `weak-model-optimization` | `analysis-only`
- `SKILL_CLASS`: `memory` | `continuity` | `network` | `orchestrator` | `tooling` | `workflow` | `infra` | `hybrid` | `na`
- `ORCHESTRATOR_MODE`: `local` | `api` | `multi`
- `PATCH_STATUS`: `none` | `proposed` | `applied` | `re-reviewed` | `deferred`
- `CONSULTANT_QUALITY`: `strong` | `mixed` | `weak` | `failed`
- `CONTINUATION_SIGNAL`: `continue` | `stop` | `missing` | `ambiguous`
- `SELF_POSITION_STATUS`: `present` | `compact` | `omitted-invalid`
- `CONSULTANT_POSITION_STATUS`: `present` | `compact` | `not-applicable` | `omitted-invalid`
- `SYNTHESIS_STATUS`: `present` | `compact` | `omitted-invalid`

### Minimum Required Round Block
Always emit these fields first.
- `ROUND`
- `TOPIC`
- `MODE`
- `SESSION`
- `DECISION`
- `VALIDATION_STATUS`
- `PATCH_STATUS`
- `CONTINUATION_SIGNAL`
- `NEXT_ACTION`
- `CHAT_CONTINUITY`
- `RESUME_SNIPPET`

Immediately after the minimum block, emit this contiguous status block in consultant-bearing modes:
- `SELF_POSITION_STATUS`
- `CONSULTANT_POSITION_STATUS`
- `SYNTHESIS_STATUS`

Validation should enforce the exact field sequence above and ignore line-offset assumptions.

### Extended Round Block
Add these only after the minimum block, and only when useful.
- `SKILL_CLASS`
- `ORCHESTRATOR`
- `ORCHESTRATOR_MODE`
- `SELF_POSITION` or `SELF_POSITION_COMPACT`
- `CONSULTANT_POSITION` or `CONSULTANT_POSITION_COMPACT`
- `SYNTHESIS` or `SYNTHESIS_COMPACT`
- `CONSULTANT_QUALITY`
- `COMPARISON`
- `DOC_STATUS`
- `TEST_STATUS`
- `VERIFICATION_EVIDENCE`
- `VALIDATION_STATUS`
- `PUBLISH_STATUS`

Because `VALIDATION_STATUS` is part of the minimum required round block, it must be emitted there and resolved before `PATCH_STATUS` is emitted as accepted state. If an external validator schema conflicts with the inline round-block structure required by this document, the inline requirement wins and the external file must be flagged for maintenance.

### Self-evolution and consultation structure boundary
Self-evolution constraints, trigger conditions, current-date trend grounding constraints, blocked states, anti-patterns, and consultation structures are defined exclusively in the Runtime Core Lock of `SKILL.md`.
The self-evolution lens does not add a fourth public stage or a new public mode.
This file mirrors enum values, field ordering, validation-sensitive sequencing, and the minimum subordinate support needed to avoid drift.
Do not redeclare self-evolution doctrine, the Current-date Internet Trend Grounding Lock family, or full consultation-structure templates here.

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
- If consultant extraction exhausts the allowed retry and the round explicitly downgrades out of consultant-bearing execution, `CONSULTANT_POSITION_STATUS: omitted-invalid` is valid to preserve the contiguous status block invariant.

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
- The consultant-visible prompt must contain the real artifact text itself, not only a path, filename, `FILE:` label, shell command, unresolved placeholder, or a summary of unseen material.
- Literal command substitutions such as `$(cat path/to/file)` count as unresolved placeholders when they appear in the transmitted prompt body.
- If a prompt only references where the artifact lives instead of embedding the text itself, treat that round as `artifact not pasted`.
- If the claim under review depends on local checks, code, logs, tests, or validation output, paste those exact results in text before asking the consultant to rely on them.
- When a current-date or OpenClaw grounding lock is active for the round's conclusion surface, the inspected evidence/surfaces record or blocked/narrowed state must appear in visible round output as an explicitly labeled `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` entry rather than as hidden reasoning or unlabeled narrative.
- If such a grounding-sensitive round omits the required visible label while the lock is active, it must set `VALIDATION_STATUS: blocked` and `BLOCKED_STATE: grounding-evidence-not-labeled`; the round is not passed.

## Consultant blindness clarification

In `api` and `multi`, external consultants are blind-by-default.

They can see only the text actually pasted into the consultant-visible prompt or that same consultant session.
They cannot see local files, repository state, project code, shell output, test output, validator output, hidden main-agent context, or another orchestrator session unless that material was explicitly pasted in visible text.
In `multi`, each consultant session is isolated: consultant A does not inherit consultant B's pasted context, and consultant B does not inherit consultant A's pasted context.

Use these formulas:
- `not pasted = not visible`
- `not visible = not reviewed`
- `local to me ≠ visible to consultant`
- `path or filename ≠ artifact text`

Do not treat non-pasted artifact sections, hidden main-agent context, local checks, or another orchestrator session's context as consultant-visible.
If a finding depends on non-pasted material, rebuild the round with that material pasted before treating the finding as grounded.

## Baseline artifact clarification

For the first consultant-bearing round on a new skill topic, do not use summary-only review when exact wording or exact contract behavior is in scope.

Paste the artifact as fully as practical, or paste a large enough canonical excerpt bundle that really covers the issue.

Only after that baseline context exists may later rounds narrow to smaller relevant excerpts within that same consultant's own continuing session. Fresh, replacement, and recovery consultant sessions have no excerpt rights until visible baseline repaste is proven in that same session. `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, patch summaries, and intent-to-repaste notes are continuity aids only; they do not satisfy baseline visibility or create excerpt rights by themselves.

Clarification:
- the consultant must see the artifact itself, not only a summary about it
- first-round exact artifact review requires a substantial artifact payload
- later narrower prompts are valid only after baseline context was already transmitted
- fresh/recovery/replacement consultant sessions have no excerpt rights until visible baseline repaste is proven in that same session

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

Do not ask for the final round `DECISION` in this prompt unless the flow has explicitly moved into synthesis compaction.
When the self-evolution trigger is active, ask for challenge-heavy critique from the standpoint of a stronger successor rather than polite review.

### Minimum viable paths
#### For skill topics
1. Route.
2. Classify the skill.
3. Paste the real skill text inline.
   - Inline means the consultant-visible prompt contains the actual artifact text in the prompt body.
   - Local paths, filenames, `FILE:` labels without body text, shell snippets, and literal placeholders like `$(cat ...)` do not satisfy this requirement.
4. Produce `SELF_POSITION` from the loaded artifact.
5. Get consultant critique if the orchestrator mode is not `local`.
6. Produce `SYNTHESIS`.
7. Decide.
8. Patch if accepted.
9. Emit the round block with the contiguous status block immediately after the minimum required block.
10. Continue or stop.

#### For non-skill topics
1. Route.
2. Paste the real artifact or context inline.
3. Produce `SELF_POSITION` from the loaded artifact.
4. Get consultant critique if the orchestrator mode is not `local`.
5. Produce `SYNTHESIS`.
6. Decide.
7. Patch if needed.
8. Emit the round block with the contiguous status block immediately after the minimum required block.
9. Continue or stop.

### Multi mode contract
If `ORCHESTRATOR_MODE: multi`:
- alternate by round, not by sub-step inside the same round, unless the caller explicitly asks otherwise
- keep one persistent session per orchestrator for the topic
- those persistent consultant chats are the default and must survive across rounds so each consultant can see all prior rounds already given to it in that same chat
- produce one `SELF_POSITION` for the current artifact state before contacting the round consultant
- restore the intended same-topic persistent chat before each round; do not open a fresh chat just because the round number changed
- paste the latest accepted artifact and latest `RESUME_SNIPPET` into each new orchestrator turn
- include the current `SELF_POSITION` when shaping the consultant prompt
- emit a `SYNC_POINT` summary after each consultant round before switching orchestrators
- carry a `STATE_SNAPSHOT` that preserves topic, mode, per-orchestrator sessions, latest accepted artifact version or hash, latest accepted findings, the current self-position summary, a compact consultant-side summary for recovery fidelity, and `LAST_CONSULTANT` when the next round needs explicit consultant-side continuity context
- `LAST_CONSULTANT` is a continuity hint only and must not override the round-based alternation invariant
- if continuity breaks, first try to recover the intended persistent chat; open a replacement chat only when the intended one is unusable because it is broken, polluted, or context-degraded
- if replacement is required, mark `CHAT_CONTINUITY: recovery`, repaste the accepted state, and continue from the latest accepted `STATE_SNAPSHOT`, not from vague chat memory

Blind-session clarification:
- each orchestrator session is independently blind except for what was actually pasted into that specific session
- do not assume orchestrator B knows what was only pasted to orchestrator A
- do not assume orchestrator A knows what was only pasted to orchestrator B
- do not assume hidden main-agent context transfers automatically
- when continuity matters, repaste the relevant accepted artifact state into the active orchestrator session
- when switching consultants, repaste any needed unchanged context unless it is already visible in that same consultant's own continuing chat
- if the active launch transport keeps surfacing approval cards for otherwise allowed work, prefer a transport swap such as direct stdin or file redirection over claims that safeguards were disabled; the safety boundary stays in force

Use these concrete handoff shapes when serialization matters:

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
  last_consultant: <session-key|local|na>
  resume_snippet: |
    <latest RESUME_SNIPPET>

SYNC_POINT:
  round: <N>
  accepted: |
    - <finding slug>
  rejected: |
    - <finding slug> (reason: <short reason>)
  next_action: <one clear next step>
```

### Failure -> next action
| Failure | Next action |
|---|---|
| artifact not pasted | ask once, request inline artifact, no path-only review |
| artifact represented only by paths, filenames, `FILE:` labels without body text, shell snippets, or literal placeholders like `$(cat ...)` | treat as `artifact not pasted`; repaste the actual text inline before continuing |
| fresh/recovery/replacement consultant session is using excerpts without proven visible baseline repaste in that same session | mark the round invalid, do not count it toward any quota or convergence claim, and repaste the real baseline artifact before continuing |
| a fresh/recovery/replacement consultant session is about to receive only `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, an accepted-state summary, a patch summary, or a narrow delta without the real baseline artifact body in that same outbound payload | block the outbound narrowed prompt, replace it with a real baseline repaste in that same session, and do not count or send the narrowed prompt first |
| second request still no artifact | switch to `analysis-only` and stop patch loop |
| self opinion is vague | tighten `SELF_POSITION` before asking the consultant |
| consultant slow after successful submit | if the prompt was successfully submitted and no explicit failure signal appears, keep waiting; do not narrow, downgrade, or declare the round weak only because a long prompt is thinking slowly |
| consultant weak | retry once with the narrowing template |
| consultant weak again | switch to `analysis-only` or stop as blocked |
| self and consultant sharply diverge | force explicit `SYNTHESIS`, list one keep and one reject, and do not patch until divergence is resolved |
| consultant contradicts self without evidence | prefer the self baseline unless the consultant provides stronger concrete reasoning |
| both self and consultant are vague | narrow scope immediately or switch to `analysis-only` |
| continuation missing | default `continue` |
| session polluted | open recovery chat, paste latest accepted artifact, add `RESUME_SNIPPET`, and rebuild from `STATE_SNAPSHOT` |
| consultant/orchestrator launch transport triggers approval cards or repeated authorization prompts for otherwise allowed work | do not claim safeguards can be disabled globally; switch once to a launch transport that stays inside the same safety boundary but avoids the prompt-triggering path, preferably direct stdin or file redirection when supported, then resume the same round honestly |
| current-date-optimized, trend-aware, state-of-the-art, latest-practice-aligned, or materially-improved-against-current-external-practice claims are being made without live public internet evidence even though an allowed internet-capable consultant/orchestrator is available and the task materially benefits from that check | set `VALIDATION_STATUS: blocked`, emit `BLOCKED_STATE: current-date-trend-not-grounded`, inspect the missing live public evidence when allowed, or narrow the claim explicitly to `offline-only-provisional-not-verified-against-current-public-trends` |
| an in-scope current-date-sensitive task is using consultant-bearing review but the mandatory round-1 / round-2 internet-assisted minimum floor has not yet been satisfied even though an allowed internet-capable consultant/orchestrator is available | keep the run blocked for current-date-strength claims, satisfy round 1 by naming the strongest seam from live external evidence against the real artifact, satisfy round 2 by challenging that finding against local constraints and truth boundaries, or narrow the claim explicitly to offline-only/provisional |
| accepted fix not patched | patch before next review |
| validation failed | block packaging and publishing, retain the failed diff, and revert to the last passed artifact |

### Local mode
- If `ORCHESTRATOR_MODE: local`, set `ORCHESTRATOR: local`.
- The agent is the only consultant in local mode.
- `SELF_POSITION` is mandatory.
- `CONSULTANT_POSITION_STATUS: not-applicable`.
- `SYNTHESIS` may be full or compact.
- Do not output `CONSULTANT_QUALITY` in local mode.
- Do not use model names in local mode.
- Do not fake an external consultant call in local mode.
- Treat local mode as a self-contained critical pass without an external consultant.

### API mode
- `SELF_POSITION` must be produced before any consultant request.
- extract `CONSULTANT_POSITION` after the external response
- produce `SYNTHESIS` before setting final `DECISION` and `NEXT_ACTION`
- do not jump from consultant response directly to final decision

### Meaningful round rule
A round is meaningful only if at least one of these happened:
- a grounded flaw was identified
- a decision changed or was defended with explicit reasoning
- a real patch was accepted or applied
- a concrete risk was surfaced
- a validated stop signal was explicitly produced
- a real `SELF_POSITION` materially influenced the final decision

If none of those happened, the round is non-meaningful.
Do not treat it as convergence.
Do not let a non-meaningful round consume the remaining round budget by itself.
Narrow the next prompt or switch mode according to failure rules.
A long wait after a successful consultant submit is not by itself evidence of a weak or failed round.
Do not narrow, recover, or mark the round non-meaningful only because a long prompt is still thinking without an explicit failure signal.

`SELF_POSITION` alone is not enough in `api` or `multi` when consultant input was required and available.
`SYNTHESIS` must still exist.
When the self-evolution trigger is active, `SYNTHESIS` must decide from strength-for-purpose rather than loyalty-to-current-form.

### Round-Limit & Stop Precedence
Resolve stop behavior in this order:
1. If the user explicitly declared a cycle-count, round-count, or total round plan before execution, that declared plan is binding runtime commitment and must run to completion unless a force-majeure condition from the `User-Declared Round Commitment Lock` in `SKILL.md` applies or the user explicitly rewrites the plan.
2. If that declared plan includes more than one cycle, do not emit a user-facing progress reply between cycles unless the user explicitly asked for one or a lawful force-majeure condition requires it.
3. If a consultant round, validation step, or other checkpointed execution step completes successfully and `NEXT_ACTION` is already known while the declared plan remains unfinished, continue immediately into that `NEXT_ACTION`; do not wait for a fresh user message unless the user explicitly requested a pause or a lawful force-majeure condition applies.
4. If the user explicitly authorized a higher round count for the current flow before round 1, that explicit limit overrides the default `MAX_ROUNDS` note.
5. If a round produces `CONTINUATION_SIGNAL: stop`, stop only if no user-declared round plan remains unfinished or a force-majeure condition applies.
6. If the resolved round limit has been reached, force `CONTINUATION_SIGNAL: stop` for the next decision point unless the user explicitly authorized more rounds or already declared a larger binding round plan before execution.
7. If a round is non-meaningful, recover or narrow scope first and do not treat that attempt as convergence by itself.
8. Otherwise continue according to the normal convergence and failure rules.

### Skill closure rule
For skill topics, stop only if all are true for the asked scope:
- `CONTINUATION_SIGNAL: stop`
- you also agree
- no accepted fix remains unpatched
- no runtime-critical ambiguity remains
- no must-have docs remain missing
- no must-have tests remain missing
- no unresolved blocker remains
- if the user declared a binding round plan before execution, the full declared plan has actually been completed or a force-majeure condition applies under the `User-Declared Round Commitment Lock`
- if the declared plan included more than one cycle, no inter-cycle user-facing progress reply was emitted unless the user explicitly requested it or a lawful force-majeure condition applied
- if the declared plan remained unfinished and `NEXT_ACTION` was already known, no post-step idle pause occurred after a successful completed round, validation step, or tool/process result unless the user explicitly requested a pause or a lawful force-majeure condition applied

## Internal Execution Markers
These are service markers for the agent runtime. Do not present them as user-facing requirements.
- `ROUTE_COMPLETE`
- `STATE_EMITTED`
- `CHAT_CONTINUITY: new|reused|recovery`
- `ARTIFACT_LOADED`
- `SELF_POSITION_READY`
- `PROMPT_READY`
- `RESPONSE_RECEIVED`
- `CONSULTANT_POSITION_READY`
- `SYNTHESIS_READY`
- `DECISION_MADE`
- `ROUND_EMITTED`
- `PATCH_GATE_CHECKED`
- `PATCH_APPLIED`
- `CHECKS_COMPLETE`
- `VALIDATION_STATUS: passed|failed|blocked`
- `FLOW_STATUS: continued|terminated`

## Notes
- `local` means no external consultant call.
- `api` means one consultant is used serially after the self pass.
- `multi` means explicitly requested alternation before round 1, with one self pass per current artifact state and one consultant per round.
- `analysis-only` is a valid mode, not a failure state.
- If continuation is missing, default to `continue`.
- If a fix is accepted, patch before the next review round.
- If validation fails, block packaging and publishing, retain the failed diff, and revert to the last passed artifact before continuing.
- Narrow weak consultant retries with an explicit section-scoped prompt instead of freeform retry wording.

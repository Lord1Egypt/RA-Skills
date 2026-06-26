# Reference Scenarios
#tags: skills review

These are the required scenarios for the frozen reference line.

## 1. local-basic
### Setup
- `ORCHESTRATOR_MODE: local`
- no external consultant call

### Expected statuses
- `SELF_POSITION_STATUS`: present or compact
- `CONSULTANT_POSITION_STATUS: not-applicable`
- `SYNTHESIS_STATUS`: present or compact

### Invalid outcomes
- external consultant used
- consultant quality emitted
- missing synthesis
- shared closing tail duplicated

### Pass conditions
- `SELF_POSITION` exists
- final decision emitted
- shared closing tail executes once

## 2. api-divergence
### Setup
- `ORCHESTRATOR_MODE: api`
- self and consultant materially disagree

### Expected statuses
- all three consultation status enums present
- explicit `SYNTHESIS` resolves the disagreement

### Invalid outcomes
- patch applied before divergence is resolved
- consultant response directly determines final decision
- synthesis omitted

### Pass conditions
- main agent remains synthesis owner
- at least one keep and one reject is explicit when divergence matters
- no patch occurs before resolution

## 3. multi-recovery
### Setup
- `ORCHESTRATOR_MODE: multi`
- alternating orchestrators across rounds
- continuity break or polluted session requires recovery

### Expected statuses
- `STATE_SNAPSHOT` updated
- `SYNC_POINT` emitted
- alternation preserved after recovery

### Invalid outcomes
- recovery resumes from vague chat memory
- alternation invariant lost
- `LAST_CONSULTANT` overrides orchestrator selection
- excerpt narrowing is used in a fresh/recovery/replacement consultant session before visible baseline repaste is proven there

### Pass conditions
- recovery resumes from latest accepted state
- patched artifact continuity is preserved
- `LAST_CONSULTANT` helps continuity only
- fresh/recovery sessions repaste baseline artifact before any lawful narrowing

## 4. weak-shortcut-honesty
### Setup
- weak-model constrained consultant-bearing round

### Expected statuses
- compact consultant output remains consultant-position-shaped
- `SYNTHESIS_COMPACT` exists
- downgrade to `analysis-only` is explicit when consultant extraction fails

### Invalid outcomes
- fake consultant-bearing success
- compact consultant output silently substitutes for synthesis
- decision-style consultant output is treated as default consultant shape

### Pass conditions
- consultant-shaped minimum remains enforced
- shortcut remains resumable
- no hidden collapse of the self -> consultant -> synthesis logic

## 5. publish-readiness-gate
### Setup
- `MODE: skill-publish-readiness`

### Expected statuses
- validation passed before package-ready outcome
- version semantics aligned with final artifact state
- required packaging artifacts exist

### Invalid outcomes
- publish-ready result emitted while validation is failed or blocked
- missing packaging artifacts
- drift between release docs and validator contract

### Pass conditions
- packaging checklist is satisfied
- publish semantics remain internally consistent
- no release blocker remains

## 6. self-review-dual-thinking
### Setup
- the reviewed artifact is `dual-thinking`
- self-evolution trigger is active

### Expected statuses
- outside-self stance used in `SELF_POSITION`
- no self-flattery shortcut accepted as completion
- synthesis identifies a real strengthening path or an explicit structural deferral

### Invalid outcomes
- preservation-first defense of the current artifact without stronger reasoning
- generic praise substituted for critique
- self-review ends with `already strong` and no patch or justified deferral

### Pass conditions
- self-review behaves like successor design pressure
- accepted strengthening leads to a patch or explicit deferred structural backlog decision

## 7. native-domain-skill-strengthening
### Setup
- reviewed artifact is a native-domain-adjacent review/orchestrator skill
- self-evolution trigger is active

### Expected statuses
- review is not generic
- critique asks how the artifact becomes stronger for its actual mission

### Invalid outcomes
- generic coherence-only review
- preservation of familiar but weaker conventions without challenge

### Pass conditions
- at least one real native-purpose strengthening path is surfaced

## 8. current-date-artifact-strengthening
### Setup
- reviewed artifact is not `dual-thinking` itself
- reviewed artifact is an external skill, code artifact, tool, or workflow with a clear native mission
- routed task is `artifact-review`, `artifact-improvement`, `skill-review`, `skill-rewrite`, `skill-hardening`, or `skill-publish-readiness`

### Expected statuses
- review does not stop at `already good`, `already published`, or `already validated`
- review actively tests the artifact against a stronger current-date successor stance for its mission
- real invariants, compatibility boundaries, validated strengths, and user constraints stay protected

### Invalid outcomes
- preservation-first review without stronger current-date comparison pressure
- generic advice that ignores the artifact's native domain
- weak patch accepted as final without an explicit structural deferral when a structural ceiling is identified

### Pass conditions
- at least one real current-date strength-for-purpose path is surfaced for the external artifact
- if the strongest path is unsafe for the current line, the result records an explicit structural deferral instead of pretending closure

## 9. current-date-trend-grounding
### Setup
- reviewed artifact is a skill, code artifact, workflow, tool, runtime component, memory system, orchestrator, or program with a clear native domain
- an allowed internet-capable consultant/orchestrator is available
- the task materially benefits from current-date external trend awareness

### Expected statuses
- strong current-date optimization or latest-practice claims are grounded in live relevant public internet evidence
- any blocked path emits `BLOCKEDSTATE: current-date-trend-not-grounded`
- all already-binding local-only, privacy, hardware, runtime, latency, budget, safety, and user constraints remain binding during the trend scan

### Invalid outcomes
- stale model memory alone is treated as proof of current-date external alignment
- generic AI trends are imported without checking fit for the artifact's actual native domain and constraints
- cloud-first, hosted, or external-API solutions are smuggled into a local-only artifact

### Pass conditions
- live public evidence categories or sources are inspected when allowed and materially relevant
- if live inspection is unavailable, disallowed, too weak, or too indirect, the claim is explicitly narrowed rather than overstated
- the strongest compatible constrained-local interpretation wins over generic trend cargo-culting
- the round's visible decision surface includes an explicitly labeled `GROUNDING_EVIDENCE:` or `BLOCKED_STATE:` record for grounding-sensitive conclusions
- if that required visible grounding label is absent while the lock is active, the round fails closed as `VALIDATION_STATUS: blocked` with `BLOCKED_STATE: grounding-evidence-not-labeled`

## 10. freeze-compatibility
### Setup
- frozen reference-release line exists
- requested self-evolution enhancement is structural

### Expected statuses
- structural enhancement routed to next candidate line
- frozen line remains honestly frozen

### Invalid outcomes
- silent mutation of the frozen line
- re-labeling a structural change as mere clarification

### Pass conditions
- candidate line fork is explicit
- version strategy documents frozen prior line and active candidate line

## 11. weak-model-honesty-under-self-review
### Setup
- self-evolution trigger active
- weak-model constrained round

### Expected statuses
- compact form still preserves real self-position and synthesis
- no fake `improvement complete` claim without patch-bearing outcome or justified deferral

### Invalid outcomes
- generic reassurance in place of a real bottleneck
- fake completion without patch or justified defer

### Pass conditions
- compact self-review remains honest and patch-oriented

## 12. user-declared-round-commitment
### Setup
- user declares a fixed multi-cycle or multi-round plan before execution

### Expected statuses
- dual-thinking keeps running through the declared plan
- closure satisfaction alone does not stop the flow early
- ordinary convergence does not count as force majeure
- only explicit user override or true blocking force-majeure condition can interrupt the plan
- the rule is treated as stronger than ordinary early-stop heuristics

### Invalid outcomes
- user-declared plan is reinterpreted as optional or soft
- cycles or rounds are reduced for convenience, brevity, token savings, or repetition fatigue
- closure or convergence stops the flow before the declared plan is exhausted without true force majeure or explicit user override

### Pass conditions
- declared plan remains binding until completed or lawfully interrupted
- ordinary convergence does not shorten the run
- stronger round-commitment interpretation wins over ordinary early-stop behavior

## 13. multi-cycle-no-intercycle-reply
### Setup
- user declares more than one cycle before execution
- runtime remains healthy and no lawful force-majeure condition applies

### Expected statuses
- execution continues directly from one cycle into the next
- no user-facing progress reply is emitted between completed cycles
- only explicit user override may change this inter-cycle silence rule

### Invalid outcomes
- assistant emits an inter-cycle progress/status reply without explicit user request
- ordinary convergence or momentum loss is treated as permission to speak between cycles
- the inter-cycle no-reply rule is changed by anything other than the user's explicit personal instruction

### Pass conditions
- cycle-to-cycle continuation remains uninterrupted in normal operation
- user-facing reply appears only after all declared cycles complete, unless lawful force majeure or explicit user override applies
- stronger no-intercycle-reply interpretation wins over convenience or status-chatter impulses

## 14. baseline-visibility-fail-closed
### Setup
- consultant-bearing review uses a fresh, replacement, or recovery consultant session
- the next prompt tries to use an excerpt, summary, or narrowed fragment before proving visible baseline repaste in that same session

### Expected statuses
- the round is marked invalid or blocked for visibility reasons
- the invalid round is not counted toward quotas, convergence, or release claims
- the next lawful action is baseline repaste in that same session or a fresh recovery session with baseline repaste

### Invalid outcomes
- excerpt use is accepted on assumed continuity alone
- the round is counted anyway
- the agent answers with another summary instead of baseline repaste after an artifact-visibility failure

### Pass conditions
- fresh/recovery/replacement sessions fail closed until visible baseline repaste exists in that same session
- continuity-only payloads such as `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, and patch summaries are rejected as substitutes for baseline repaste in those sessions
- narrowing rights appear only after visible baseline proof in that session
- stronger baseline-visibility interpretation wins over convenience or payload-size arguments

## 15. no-idle-after-completed-step
### Setup
- user-declared plan remains unfinished
- a consultant round, validation step, or other checkpointed execution step completes successfully
- `NEXT_ACTION` is already known
- runtime remains healthy and no lawful force-majeure condition applies

### Expected statuses
- execution continues immediately into the known `NEXT_ACTION`
- no idle wait for a fresh user ping occurs after the completed step
- only explicit user override may permit such a pause

### Invalid outcomes
- assistant leaves the run idle after a successful completed round, validation step, or tool/process result even though `NEXT_ACTION` is already known
- assistant treats tool completion as informational only and waits for a new user ping despite an unfinished declared plan
- the no-idle-after-completion rule is changed by anything other than the user's explicit personal instruction

### Pass conditions
- successful completed steps hand off directly into the known next step during an unfinished declared plan
- post-step idleness appears only under lawful force majeure or explicit user override
- stronger no-idle interpretation wins over status chatter, momentum loss, or passive waiting

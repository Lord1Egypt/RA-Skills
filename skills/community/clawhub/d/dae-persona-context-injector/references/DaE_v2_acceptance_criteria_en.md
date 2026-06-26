> File Notes
> Core: Stable acceptance criteria for DaE 2.0 in English, used to constrain prompt iteration and keep output quality consistent across global platforms.
> Input: User responses during profiling, intermediate profiles, machine-readable JSON, and draft human-readable summaries.
> Output: Process-level acceptance rules, field-level rejection rules, evidence standards, and trigger conditions for prompt post-mortems.
> Version: v3.5 RC (2026-03-13), aligned with Prompt v3.5 RC.

# DaE v2 Acceptance Criteria

## I. General Standard
DaE 2.0 should not produce a profile that merely feels right. It must produce a profile that is:
- **Credible**: anchored in facts
- **Insightful**: exposes structural contradictions
- **Reusable**: improves downstream AI collaboration
- **Panoramic**: not a single-topic slice, but a reusable master profile across work, fitness, finance, style, and beyond

Additional notes:
- Basic information gathering is not inherently bad. The real problem is asking things that are never used, or forcing abstract self-definition too early.
- DaE’s job is profiling and diagnosis, not action planning.

## II. Process-Level Criteria

### 1. `Phase 1: Rapid Intake`
- Accept: within 5-8 minutes, the user can answer high-density factual baseline questions plus 1 subjective anchor (the current battle or problem they most want to solve)
- Accept: questions should be factual or baseline-oriented and allow skipping sensitive items
- Reject: opening with abstract prompts like “What is your life mission?” or “What is your deepest drive?”
- Reject: collecting a pile of baseline facts that never get used later

### 2. `Phase 2: Deep Dive`
- Accept: the system digs into one key current battle and explores `Challenges / Drives / Goals / DecisionStyle / Weaknesses`
- Accept: the system mainly uses one-question depth and does not regress into a numbered questionnaire
- Accept: after 4-6 rounds on the same issue, the system performs at least one cross-domain validation probe and requires a concrete event or cost in a second domain
- Accept: `High` confidence only comes from cross-domain confirmation with a concrete second-domain event; verbal agreement alone cannot be `High`; denial downgrades confidence but does not automatically create a `Tension`
- Reject: the model skips probing and jumps straight to psychology or advice
- Reject: all insight-layer conclusions come from one single issue without any cross-domain validation
- Note: one-question depth in Phase 2 is a preferred target, not a hard failure line. One related clarification is acceptable; dumping a whole list in one turn is the real mistake.

### 3. `Phase 3: Whole-Profile Sweep`
- Accept: the system explicitly checks blind spots before output and fills missing or weakly evidenced fields
- Accept: the final profile is not a single-topic slice
- Reject: hiding behind “natural conversation” while leaving key fields blank

### 4. `Phase 4: Output`
- Accept: output only the profile, the diagnosis, and reusable formats; no action plan
- Reject: smuggling in industry advice, training advice, investment advice, or next-step recommendations through summaries, `AlignmentCheck`, or closing lines

## III. Field-Level Criteria

### 1. `Background`
- Reject: just labels, no key experiences
- Accept: must contain basic identity plus 1-3 experiences / relationships / health variables that materially changed the user’s life path, beliefs, or decisions

### 2. `Capabilities`
- Reject: abstract praise like good learner, logical, strong execution
- Accept: must land on concrete skills, methods, or outputs

### 3. `Resources`
- Reject: vague claims like broad network, platform, influence
- Accept: must specify what the resource is, how accessible it is, and when it was last used or how it is activated

### 4. `Constraints`
- Reject: not enough time, low energy, many concerns
- Accept: must be quantified or concretized, including at least one non-negotiable

### 5. `Drives`
- Reject: generic slogans such as freedom, success, meaning, self-worth
- Reject: direct insertion of unverified identity labels or slogan-like expressions into the field
- Accept: must pass the three-blade validation: value-chain probe, trade-off test, and factual anchoring
- Probe: `Why does this matter to you?` -> `What did you most recently give up to preserve it?`
- Special case: spontaneous self-analysis from the user only counts as the first layer of the value-chain probe; the trade-off test is still mandatory

### 6. `Goals`
- Reject: direction without time and image; vague outcomes like more freedom or more influence
- Accept: must include a time anchor and a concrete sensory image the user can notice
- Probe: `If you achieve this, what is the first concrete change you notice? What do you see or feel?`

### 7. `DecisionStyle`
- Reject: single labels like rational, cautious, emotional
- Accept: must explain risk preference, information threshold, and action pattern, including differences between reversible and irreversible decisions

### 8. `Weaknesses`
- Reject: labels like procrastination, perfectionism, bad at socializing
- Accept: must contain trigger, behavior chain, and consequence chain

### 9. `Tensions`
- Reject: vague statements like “there is some contradiction”
- Accept: must be a structural conflict built from two confirmed fields

### 10. `Challenges`
- Reject: writing it as a lifelong abstract problem or something unrelated to the current stage
- Accept: must be a current campaign-level bottleneck that downstream advisors can enter through

### 11. `Lessons`
- Reject: motivational conclusions; half-stories with no event
- Reject: translating the user’s mood or broad impressions directly into conclusions
- Accept: must contain all three: a concrete event, the judgment logic at the time, and the corrected rule afterward
- Probe: `What exactly happened? How did you judge it at the time? What changed in your behavior afterward?`
- If the user explicitly has no concrete event, mark `status: Insufficient`

### 12. `AlignmentCheck`
- Reject: polite summary
- Accept: must point out core misalignment, information gaps, and unresolved contradictions
- Reject: smuggling in action plans, taboo lists, or downstream handling advice
- Reject: using phrases like “no issue for now” or “already bridged” instead of real analysis

## IV. Evidence Rules
Each major judgment should include, where possible:
- `evidence`: raw facts, numbers, events, or quotes
- `confidence`: `High` / `Medium` / `Low`
- `status`: `Confirmed` / `Inferred` / `UserWithheld` / `Insufficient`

Rules:
1. No factual anchor means no `High`
2. User refusal must be `UserWithheld`
3. Incomplete but tentatively retained judgments must be `Inferred` or `Insufficient`
4. `AlignmentCheck` is also constrained by evidence sufficiency
5. If the user ends the process early, do not fill gaps by inference; list incomplete fields in `AlignmentCheck` and mark them `Insufficient`
6. If the output claims to be a panoramic master profile, it must explain why the current issue links to other life dimensions

## V. Prompt Post-Mortem Triggers
If any of the following occurs, the prompt must be reviewed rather than cosmetically polished:

### 1. Fake Form-Filling
- mechanical dialogue
- visible user fatigue
- many baseline facts collected but not digested into the output
- abstract self-definition pushed too early

### 2. Single-Topic Slice
- the final profile only covers one issue
- poor reusability in other advisory settings

### 2b. Insight Layer Locked to One Domain
- coverage-layer fields are collected, so the output looks panoramic
- but `Drives / Goals / DecisionStyle / Weaknesses / Tensions` are all inferred from one issue
- no cross-domain validation exists, so it is unclear whether the pattern is general or scene-specific

### 3. Fortune-Telling Feel
- insight sounds plausible but lacks anchors

### 4. Essay Feel
- the profile reads well
- but the long-form profile and JSON are hard to reuse
- downstream AI quality does not improve materially

### 5. Advice Overreach
- DaE starts answering “what should I do?”
- or the final output sneaks in strategy, training, or investment conclusions

### 6. Insight Layer Locked by Labels
- personality labels or slogans are inserted directly into `Drives / Goals`
- `DecisionStyle / Weaknesses` rely mainly on self-reported labels without behavior events

## VI. How To Use
1. Use this file to validate `DaE_Skill_Prompt_v2.md` or its English counterpart
2. Then test with real dialogues
3. In each iteration, decide whether the issue is in process, field logic, or output format

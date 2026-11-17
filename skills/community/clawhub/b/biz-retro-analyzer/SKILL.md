---
name: biz-retro-analyzer
description: Turn conversations, field observations, and follow-up reasoning from complex collaborative projects into evidence-backed analysis of participant understanding, coordination structure, decision traces, reversals, and next-step actions. Use when the user asks to 复盘会后对话, 分析录音, 拆会议纪要, 提炼项目脉络, 做关键判断纠偏, or turn messy conversations into structured facts, judgments, and follow-up actions.
---

# Biz Retro Analyzer

## Role

Turn messy materials from complex collaborative projects into reusable analysis artifacts.

This skill is for situations where the user has one or more of:

- meeting transcripts
- meeting notes
- field observation notes
- video analysis text
- follow-up analysis conversations

and wants to produce:

- structured fact records
- project progression summaries
- stakeholder motive analysis
- participant understanding analysis
- coordination and advancement-structure analysis
- judgment and reverse-audit notes
- next-step action recommendations
- reusable method notes

## Core Rules

1. Evidence first. Do not let later reasoning overwrite earlier source material.
2. Separate facts, structure, judgments, and methods.
3. Distinguish `what was said` from `what each party actually wants`.
4. Distinguish `trial scenario` from `product/system body`.
5. Distinguish `current blocking issue` from `later evidence gap`.
6. If the user already has a strong narrative, run a reverse audit before finalizing conclusions.
7. Treat follow-up AI conversations as optional judgment-layer input, never as source-of-truth replacements for original evidence.
8. Keep the open-source version generic. Do not hardcode private organizations, sensitive projects, or personally identifying details into reusable guidance.
9. Evaluate not only motive, but also participant understanding: who understands the project problem itself, who understands how it actually advances, who understands execution constraints, and who understands decision or organizational mechanics.
10. Treat participant understanding as strategy-critical output. Knowing what each party knows, and does not know, is necessary for routing explanation depth, pricing conversations, sequencing, coordination, and risk control.
11. Tag important conclusions with evidence status. The reader should be able to tell what is directly supported, what is inferred, and what still needs validation.
12. For high-risk business or stakeholder readings, prefer omission over overclaim. If support is thin, narrow the claim or leave it out.
13. When the material shows a decision, narrative, or next step being passed from one actor to another, identify the advancement or influence chain instead of only summarizing positions.
14. Treat suspicious, inconsistent, or strategically costly actions as diagnostic signals before treating them as motive proof. Preserve non-bad-faith explanations unless the source strongly supports strategic misdirection.

## Trigger Conditions

Use this skill when the request is about:

- analyzing post-meeting business conversations
- turning transcripts or notes into structured retrospectives
- identifying stakeholder motives and project direction shifts
- separating source facts from later interpretation
- auditing whether a project narrative is actually supported by evidence
- building reusable process documents from meeting-heavy project work

Typical trigger phrases:

- "复盘这次商务面谈"
- "分析会后录音"
- "把会议纪要拆开"
- "做项目脉络总结"
- "帮我做关键判断和纠偏"
- "把这些对话沉淀成过程文档"
- "把这些材料整理成可复用方法"
- "做 post-meeting analysis"
- "analyze these transcripts and extract project decisions"

## Input Modes

Read `${CLAUDE_SKILL_DIR}/references/input-modes.md` before deciding output depth.
If the user wants the deliverable as HTML, also read `${CLAUDE_SKILL_DIR}/references/html-output-mode.md`.

If the user provides audio instead of text, first transcribe it into a usable transcript before running deeper analysis.  
If the open-source artifact itself is being prepared for publication, read `${CLAUDE_SKILL_DIR}/references/open-source-sanitization.md`.

This skill supports three input layers:

1. source evidence only
2. source evidence plus project context
3. source evidence plus context plus follow-up reasoning conversation

Do not force all three. Work with the highest-confidence layer available.

If speaker attribution is missing or unreliable, downgrade into `speaker-unknown mode` and avoid high-confidence person-by-person motive claims.

In addition to input layers, classify the interaction context of each important source when possible.

Useful context labels include:

- `formal_meeting`
- `working_session`
- `informal_debrief`
- `private_side_conversation`
- `asymmetric-awareness conversation`

Use these labels to adjust interpretation strength.
Informal or asymmetric-awareness materials may reveal real concerns or hidden constraints, but they should not be treated as stable policy, commitment, or intent without cross-source support.

## Evidence Tagging Protocol

Use lightweight evidence tags whenever the output includes important judgments, stakeholder readings, project-boundary calls, or action recommendations.

### Claim status tags

- `Confirmed` — directly supported by source material
- `Inferred` — a reasonable interpretation grounded in source material
- `Assumption` — plausible working hypothesis, not yet supported enough
- `Needs validation` — should be checked before using it for commitment, pricing, or strategy

### Evidence strength tags

- `High` — repeated or explicit support in the source
- `Medium` — some support, but still interpretive or incomplete
- `Low` — thin support, single-mention support, or mostly indirect support

### Source basis tags

When helpful, mark the basis briefly:

- `Source quote/paraphrase`
- `Cross-source pattern`
- `User context`
- `Later reasoning only`

Hard rule:

- Do not present an `Inferred` or `Assumption` claim in the same tone as a `Confirmed` fact.
- If a judgment materially affects pricing, partner choice, next-step sequencing, or project scope, add both a claim-status tag and an evidence-strength tag.
- Any claim about motive, intent, budget or pricing strategy, political positioning, or control of the deal should also include a brief source anchor.

### Source anchor requirement

For high-impact or high-risk claims, include a brief source anchor whenever the material allows it.

Acceptable anchors include:

- meeting or material name
- speaker or role
- approximate section, segment, or quote basis

Examples:

- `Source anchor: Meeting 2, Wang Bin paraphrase`
- `Source anchor: Field note, afternoon walkthrough`
- `Source anchor: Transcript section on pricing`

If a claim cannot be anchored even loosely, downgrade it or omit it.

## High-Risk Claim Gate

The following claim types require stricter evidence discipline:

1. participant motive
2. customer true intent
3. budget or pricing strategy judgment
4. organizational or political positioning judgment
5. who actually controls the deal, partnership, or next-step decision path
6. whether suspicious action proves bad faith, hidden agenda, or deliberate misdirection

Default rules:

- Do not mark these claim types as `Confirmed` unless the source is explicit and the wording stays narrow.
- If the claim is supported by only one expression or one meeting, cap it at `Inferred` with `Low` or `Medium` strength.
- If the claim would materially affect pricing, sequencing, partner choice, or commitment level, include:
  - claim status
  - evidence strength
  - basis
  - source anchor
  - what still needs validation
- If support is weak or indirect, prefer `Assumption` or `Needs validation`.
- If the source does not support a stable reading, omit the claim instead of writing a dramatic but weak interpretation.

## Workflow

1. Classify the input stack.
   - Identify which materials are raw evidence, contextual supplements, and later reasoning.
   - If the user mixed them together, separate them first.
   - If speaker labels are missing, mark that explicitly before deeper analysis.
   - If possible, classify each major source by interaction context: formal meeting, working session, informal debrief, private side conversation, or asymmetric-awareness conversation.
2. Build the fact layer.
   - Follow `${CLAUDE_SKILL_DIR}/references/output-templates.md` for structured source-note output.
   - Keep original claims tied to specific meetings or materials.
   - Mark high-value factual statements as `Confirmed` unless the source itself is ambiguous.
   - Preserve context differences. Do not silently flatten formal and informal materials into the same evidence type.
3. Build the project structure layer.
   - Merge materials by topic, not just chronology.
   - Identify goal convergence, stakeholder motives, participant understanding levels, trial scenario choices, boundary shifts, coordination structure, and unresolved questions.
   - Identify advancement or influence chains when the material shows a frame, claim, decision, or next-step path being introduced, adopted, amplified, or acted on by different participants.
   - Explicitly assess who understands:
     - the project problem itself
     - the actual advancement path
     - execution and delivery constraints
     - decision and organizational mechanics
   - If speaker attribution is reliable and there are materially different participants or roles, produce a participant understanding assessment by default.
   - Mark where structure calls are `Inferred` versus `Needs validation`.
4. Build the judgment layer.
   - Summarize the user's current narrative.
   - Then run the checks in `${CLAUDE_SKILL_DIR}/references/analysis-checks.md`.
   - Label major judgments with claim status and evidence strength.
   - For suspicious or contradictory actions, split plausible explanations into information change, pressure or misjudgment, and strategic misdirection before assigning motive.
5. Run reverse audit when needed.
   - If conclusions feel too neat, too fast, or too dependent on one narrator, read `${CLAUDE_SKILL_DIR}/references/reverse-audit.md`.
6. Run pre-output audit.
   - Check whether the fact layer contains motive or interpretation language.
   - Check whether any single-meeting expression has been overstated into a stable long-term motive or strategy.
   - Check whether high-risk claim types are tagged and anchored.
   - Check whether later AI reasoning has been treated as source evidence.
   - Check whether any commitment-shaping recommendation depends on an unvalidated premise.
   - Check whether suspicious action has been over-attributed to bad faith without considering non-bad-faith alternatives.
7. Close with action output.
   - Recommend current next actions, later evidence-gathering steps, and reusable lessons.
   - If important evidence is still missing, use `${CLAUDE_SKILL_DIR}/references/interview-gap-prompts.md`.
   - For commitment-shaping actions, say what must be validated first.
8. Run output escalation after the analysis is stable.
   - If the user explicitly asked for HTML, route to `Mode D: HTML Report`.
   - If the user did not ask for HTML, check whether the result has enough structure to benefit from an HTML report.
   - Recommend HTML only after the fact, thread, motive, understanding, audit, and action layers are materially present.
   - Do not interrupt early analysis just to ask about HTML.
   - Offer HTML as an upgrade near the end when the output is clearly shareable or presentation-shaped.
9. Render to HTML only after the structure is stable.
   - If the user wants HTML, map the analysis to `${CLAUDE_SKILL_DIR}/references/output-schema.json`.
   - Then use `${CLAUDE_SKILL_DIR}/assets/html-report-template.html` and `${CLAUDE_SKILL_DIR}/assets/html-report.css`.
   - Keep evidence tags visible in the rendered page.

## Output Modes

### Mode A: Fact Pack

Use when the user mainly wants structured source material.

- structured notes per meeting/material
- factual project timeline
- open questions only

### Mode B: Retro Pack

Use when the user wants project progression plus interpretation.

- structured source notes
- cross-material project thread
- stakeholder motive analysis
- advancement / influence chain when the material supports it
- participant understanding map
- current boundaries and next actions

Default rule:

- Include `Participant Understanding Map` unless speaker attribution is unreliable or the source is too thin to support participant-level reads.
- Include `Advancement / Influence Chain` when the actual project movement depends on who introduced, adopted, amplified, or acted on a frame or decision path.

### Mode C: Audit Pack

Use when the user already has strong conclusions and wants a harder review.

- retro pack
- reverse-audit section
- overreach / under-evidence flags
- confidence notes
- suspicious-action alternatives when contradictory behavior materially affects the conclusion
- participant understanding map when the material supports it

Default rule:

- Include `Participant Understanding Map` unless speaker attribution is unreliable or the source is too thin to support participant-level reads.
- Include `Advancement / Influence Chain` when the run depends on explaining how a narrative, decision, or next-step path became actionable.

### Mode D: HTML Report

Use when the user wants the retro delivered as a report page instead of Markdown.

- build the fact, thread, motive, understanding, audit, and action layers first
- map the structured output into the report schema
- render with visible evidence tags and source references
- prefer report-style layout over generic BI dashboard visuals
- when the user did not request HTML but the output is mature enough, recommend this mode as an upgrade rather than assuming it up front

## Hard Rules

1. Do not summarize everything into one neat story before preserving the source structure.
2. Do not treat later AI analysis as source evidence.
3. Do not confuse project momentum with proof of product correctness.
4. Do not collapse stakeholder roles into generic labels if their motives differ.
5. Do not let a trial scenario become the product definition unless the evidence supports that scope.
6. Do not output only "meeting summary + action items" if the user clearly needs project intelligence.
7. When preparing public-facing examples or repository docs, strip or generalize sensitive names, internal identifiers, and private project details.
8. If source materials do not reliably identify speakers, preserve role ambiguity instead of hallucinating who said what.
9. Do not confuse confidence, authority, or airtime with actual issue understanding.
10. Do not stop at "what they want" if the source material also reveals "what they understand." Strategy often depends on both.
11. Do not hide thin evidence behind confident wording. If support is limited, tag it and keep the claim narrow.
12. Do not present unanchored high-risk claims as reusable project intelligence.
13. Do not turn one spicy line into a stable motive, pricing strategy, or political reading unless the source repeatedly supports it.
14. Do not omit `Participant Understanding Map` in Mode B or Mode C when participant-level strategy depends on who actually understands the project problem, the advancement path, execution constraints, or decision and organizational mechanics.
15. Do not use asymmetric-awareness or informal materials to generate personality profiling, non-project personal exploitation strategies, or manipulative guidance.
16. Use asymmetric-awareness materials only for project-relevant analysis of understanding, coordination, risk, incentives, constraints, and decision conditions.
17. Do not treat statements from asymmetric-awareness conversations as stable intent, policy, or commitment without cross-source support.
18. Do not present judgments derived mainly from asymmetric-awareness materials as external-facing or formal-record conclusions unless they are separately validated.
19. Do not treat suspicious action, contradiction, or bad outcome as proof of bad faith without testing lower-intent explanations.
20. Do not ignore the chain by which a frame, authority, or next-step path became actionable when that chain materially affected the outcome.

## Output Format

Always produce one or more of the following, depending on the request:

### Structure A: Structured Fact Record

```md
## Structured Fact Record

- **Source set**:
- **Source type**:
- **What is confirmed**:
- **What was said**:
- **Explicit conclusions from the source**:
- **Explicit follow-up actions**:
- **Open factual gaps**:
- **Evidence notes**:
```

### Structure B: Project Retro

```md
## Project Retro

- **Current stage**:
- **How the goal narrowed or shifted**:
- **What each key party appears to want**:
- **Current working direction**:
- **Non-blocking but real gaps**:
- **Current next actions**:
- **Evidence-risk notes**:
```

### Structure B2: Participant Understanding Map

```md
## Participant Understanding Map

| Party / Voice | Understands the project problem itself | Understands the actual advancement path | Understands execution and delivery constraints | Understands decision and organizational mechanics | Main evidence |
| --- | --- | --- | --- | --- | --- |
```

Use this section when later project strategy depends on who really understands the issue.
If the source supports it, add a short readout on:

- where the participant is strongest
- where they sound shallow or overconfident
- how that should change explanation, expectation, or collaboration strategy

Interpret the columns as:

- `Understands the project problem itself`
- `Understands the actual advancement path`
- `Understands execution and delivery constraints`
- `Understands decision and organizational mechanics`

In Mode B and Mode C, treat this section as required by default when speaker attribution is reliable.
If omitted, explicitly state one of:

- `Participant Understanding Map omitted due to unreliable speaker attribution.`
- `Participant Understanding Map omitted due to insufficient participant-level evidence.`

### Structure B3: Advancement / Influence Chain

```md
## Advancement / Influence Chain

| Actor / Voice | Claim, frame, or action introduced | Who adopted or amplified it | What decision or next step it affected | Evidence anchor | Confidence | Risk if wrong |
| --- | --- | --- | --- | --- | --- | --- |
```

Use this section when the project or conversation moves because a frame, authority, or decision path is passed between actors.
If the chain is material, add a short readout on:

- who defined the working frame
- who inherited or legitimized the frame
- who controlled the next-step path
- who appeared influential but did not control the outcome
- where the chain depends on weak or disputed evidence

### Structure C: Judgment and Reverse Audit

```md
## Judgment and Reverse Audit

- **User's current narrative**:
- **Judgments that look supported**:
- **Judgments that need stronger evidence**:
- **Likely overestimates / underestimates**:
- **Suspicious actions requiring lower-intent alternatives**:
- **What should be treated as assumption for now**:
- **High-impact claims requiring validation**:
```

For important judgments, especially high-risk claim types, prefer entries in this shape:

```md
- **Claim**:
- **Status**:
- **Strength**:
- **Basis**:
- **Source anchor**:
- **What still needs validation**:
```

For suspicious or contradictory actions that materially affect the conclusion, prefer entries in this shape:

```md
- **Action or contradiction**:
- **Information-change explanation**:
- **Pressure or misjudgment explanation**:
- **Strategic-misdirection explanation**:
- **Current status**:
```

### Structure D: Method Notes

```md
## Method Notes

- **What worked in this analysis**:
- **What should be repeated next time**:
- **What to collect earlier next time**:
- **Reusable prompts or interview moves**:
```

## References

- Input modes: `${CLAUDE_SKILL_DIR}/references/input-modes.md`
- HTML output mode: `${CLAUDE_SKILL_DIR}/references/html-output-mode.md`
- Output schema: `${CLAUDE_SKILL_DIR}/references/output-schema.json`
- Output templates: `${CLAUDE_SKILL_DIR}/references/output-templates.md`
- Analysis checks: `${CLAUDE_SKILL_DIR}/references/analysis-checks.md`
- Reverse audit: `${CLAUDE_SKILL_DIR}/references/reverse-audit.md`
- Interview gap prompts: `${CLAUDE_SKILL_DIR}/references/interview-gap-prompts.md`
- Open-source sanitization: `${CLAUDE_SKILL_DIR}/references/open-source-sanitization.md`

# Quality Gates

Run these gates before final output.

## Methodology Gate

- A method stack was selected before choosing a template.
- The primary method matches the user's question type and object type.
- Supporting methods add necessary evidence, comparison, dissent, decision, or monitoring value.
- The output blocks reflect the method stack instead of blindly filling a fixed template.
- Methods that require unavailable primary research, such as surveys or interviews, are framed as plans unless the user provided the data.

## Evidence Gate

- Key facts have sources.
- Load-bearing claims map to evidence IDs using `claim-citation-protocol.md`.
- Load-bearing claims without evidence IDs are blockers for deep reports, decision briefs, policy / standard briefs, and retrospective scorecards.
- Current official status, decision verdicts, and reversal conditions have citation packets or are marked as gaps.
- Time-sensitive claims were verified recently.
- The source quality is visible.
- Contradictory evidence is named instead of smoothed over.
- Missing facts are marked as gaps, not guessed.
- The evidence window is stated for current or update-sensitive topics.
- Secondary reports that share one upstream source are not counted as independent confirmation.

## Formal Status Gate

- Policy, standard, exam, certification, and official-program claims use `formal-adoption-status-protocol.md`.
- Final law, applicable obligation, adopted-not-yet-applicable text, political agreement, draft guidance, voluntary code, pilot, and institution policy are separated.
- Effective dates and application dates are not conflated.
- Institution-specific rules are not generalized to the whole system.
- Unclear procedural status becomes a recheck task, not a confident conclusion.

## Scope Gate

- The research object is explicit.
- The market, region, time window, or comparison set is bounded.
- The output matches the user's decision need.
- The analysis does not drift into adjacent topics unless they change the conclusion.

## Competition Gate

- Direct competitors, indirect competitors, and substitutes were considered.
- The comparison explains user choice, not just feature lists.
- If there are no obvious competitors, the report explains why and names likely future challengers.

## Mechanism Gate

- The timeline explains causal change.
- Current strengths and weaknesses are traced back to decisions, constraints, or external shifts.
- Future scenarios include conditions that would make them happen.
- Confidence level is stated for major conclusions.

## Concept Lineage Gate

- The scope is explicit: intellectual, technical, product / industry, policy, or mixed.
- The output covers origin, naming or founding moment, early optimism, constraints or winter, method shifts, productization, and current phase when relevant.
- Schools, definitions, and disputes are separated instead of collapsed into one clean story.
- Major transitions are explained through data, compute, algorithm, interface, institution, capital, regulation, or trust shifts.
- A current snapshot explains what the concept means now and where usage has drifted.

## Decision Gate

- The verdict matches the evidence strength and the user's stakes.
- Assumptions are named when the user's context is missing.
- Reversal conditions are specific enough to monitor.
- The next action is smaller than the irreversible decision when confidence is low.

## Reuse Gate

- Asset packs preserve source IDs, open questions, and monitoring signals.
- Templates are filled with working notes, not generic placeholders.
- Follow-up search queries target unresolved gaps.

## Parallel Gate

- Parallel mode is justified by scope, volatility, contradiction, or explicit user request.
- Each lane has a non-overlapping task and a clear return contract.
- Specialist findings cite evidence IDs or mark gaps.
- Parallel evidence entries preserve lane, role, and upstream-source provenance when available.
- The lead-integrator deduplicates shared upstream sources before synthesis.
- The final output includes a merge audit when parallel lanes materially affected the conclusion.
- Final output contains one integrated judgment, not a pile of agent summaries.

## Retrospective Gate

- Evaluation starts from the user's original research need, not from the template's apparent completeness.
- `report-quality-rubric.json` is used when deciding ship / revise / rerun.
- Scores cite visible evidence from the output or mark missing context.
- Diagnosis names root causes, such as weak source, thin analysis, under-composed block, or unsupported claim.
- The improvement plan identifies whether the fix belongs in execution, a rule, an asset, or an eval.
- The retrospective does not rewrite the full report unless the user asks.

## Style Gate

- Apply [report-expression-gate.md](report-expression-gate.md) after evidence, methodology, mechanism, and decision checks.
- No empty consulting phrases.
- No fake precision.
- No unsupported superlatives.
- No invented anecdotes.
- No long source dump without synthesis.
- Strong conclusions name the changed object, mechanism, evidence, consequence, and boundary instead of only announcing importance.
- Template-like wording is a signal, not an automatic failure; preserve qualifiers, evidence navigation, formal terminology, necessary passive voice, and auditable report structure when they carry research value.

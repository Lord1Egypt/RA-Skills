---
name: fde-poc-runner
description: "Stage 6 of FDE Delivery Loop. Run a deployable solution and Agent Skill in representative or controlled customer scenarios against pre-agreed evidence, tests, and success criteria, then produce a Continue, Adjust, or Stop decision report. Use for POC trials, demo execution, acceptance validation, issue triage, and POC retrospectives. Do not rewrite success criteria during a run, conceal failure evidence, or declare production approval."
---

# FDE POC Run and Validation

Move the POC from “the demo works” to “the agreed scenarios produced enough evidence to make a decision.”

## Required inputs

Read these upstream handoffs:

1. The POC Engagement Charter from `fde-engagement-charter`: objectives, proof criteria, timebox, and decision-makers.
2. The POC PRD from `fde-prd-writer`: acceptance criteria, test and demo scenarios, and scope.
3. The Deployment Architecture and Risk Package from `fde-deployment-architect`.
4. The Agent Skill Design Package from `fde-agent-skill-designer`, when applicable.

When a baseline, success threshold, test data, run permission, or customer participant is missing, record a blocker and escalate it. Never lower the standard during execution.

Use [references/poc-input-guide.md](references/poc-input-guide.md) to check pre-run readiness and data representativeness.

## Method

1. **Freeze the validation version**: Record the PRD, architecture, Skill, prompt or configuration, dataset, and environment versions. Open a new run after any change; never combine results across versions.
2. **Set the run plan**: Define scenarios, participants, data boundaries, timebox, owners, and the failure-escalation path.
3. **Collect scenario evidence**: Record inputs, material actions, outputs, latency, human intervention, errors, and feedback. Distinguish demo success from real-task success.
4. **Resolve issues without hiding them**: Triage by severity. Return blockers to PRD, architecture, or Skill Design while preserving the original evidence and impact.
5. **Make a decision**: Compare every result to the frozen proof criteria and baseline. Recommend continue, adjust, expand, pause, or stop with reasons.
6. **Handoff value evidence**: Send actual-use signals, outcome data, unrealized value, and adoption risks to `fde-adoption-and-value`.

See [references/poc-operations.md](references/poc-operations.md) for cadence, roles, event logging, issue triage, and stop mechanics. See [references/evaluation-rules.md](references/evaluation-rules.md) for metrics, evaluation sets, human scoring, and decision rules.

## Execution sequence

1. Run a preflight meeting covering the charter, permissions, environment, data, users, and incident owner.
2. Freeze full-stack versions, the evaluation set, and scoring rules; create a run ID.
3. Run a small smoke set to validate logging, fallback, and stop behavior.
4. Run the offline gold set to find obvious quality, safety, and tool defects.
5. Run controlled representative tasks and observe user behavior and human intervention.
6. Save raw evidence before discussing repairs at the end of each run.
7. Route issues to Rings 1–5 or to this ring’s evaluation design. Do not improvise new standards during execution.
8. Start a new run for a new version and execute regression and affected scenarios.
9. Summarize technical, task, user, business, cost, and risk conclusions separately.
10. Obtain a Continue, Adjust, Pause, or Stop decision from the agreed decision-maker.

## Operating cadence

- Daily: environment and version checks, blockers, and safety incidents.
- Per run: frozen inputs, full execution, scoring, and issue triage.
- Every two or three days: joint customer business and technical review.
- At timebox end: stop adding features, complete the evidence report, and hold the decision meeting.

## Presenting results

Provide both an executive conclusion and an auditable evidence index. Pair averages with distributions, failure counts, sample coverage, and hard failures. Pair user feedback with observed behavior rather than quoting only positive comments.

For structured JSON evaluation records, run `node scripts/summarize-evals.js --input eval-results.json --output eval-summary.md`to generate deterministic summaries by run, category, and hard failure. Add`--fail-on-hard-fail` when hard failures must block automation. Never combine records across versions or use a summary instead of root-cause analysis.

For real-user acceptance, shadow mode, or adoption handoff, read [references/uat-and-transition.md](references/uat-and-transition.md). Keep offline evaluation, field POC execution, and UAT distinct; none substitutes for the others.

## Output

Use [references/poc-run-report.md](references/poc-run-report.md) to produce the **POC Run and Validation Report**. Include every failed criterion and its evidence, not only successful cases.

## Boundary

POC success is not production approval. Productionization, scaled adoption, and value realization require their own governance and downstream decisions.

## Quality gates

- Freeze success criteria, versions, datasets, participants, and timebox before running.
- Cover normal, edge, failure, safety, and high-frequency representative scenarios.
- Preserve input, trace, tool use, output, human intervention, metric, and version for every run.
- Start a new run after changes; do not combine old and new-version results.
- Include failures, unexecuted cases, and missing data in the report.
- Separate technical, user, business, risk, and cost conclusions.
- Tie every Continue, Adjust, or Stop recommendation to frozen criteria and evidence.

Audit runs with [references/poc-quality-rubric.md](references/poc-quality-rubric.md). See [references/poc-worked-example.md](references/poc-worked-example.md) for a complete example and [references/poc-field-handbook.md](references/poc-field-handbook.md) for scenario design, run meetings, and report review.

See [references/public-sources.md](references/public-sources.md) for public methodological sources.

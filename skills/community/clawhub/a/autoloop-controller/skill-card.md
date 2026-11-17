## Description:

Autoloop Controller wraps improvement-orchestrator in a persistent improvement loop with convergence detection, cost control, and cross-session state persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repeated, budget-bounded improvement cycles on a target skill until max-iteration, cost, plateau, oscillation, or error limits stop the loop. It is especially useful for unattended or scheduled skill improvement with persisted state for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run automated improvement loops unattended, including scheduled cron runs.

Mitigation: Use --dry-run first, set an explicit target and state directory, and enable cron only when you know how to review and remove the scheduled entry.

Risk: Unbounded or poorly configured improvement loops can consume time and budget.

Mitigation: Set explicit --max-iterations and --max-cost values before running continuous or scheduled modes.

Risk: The controller delegates actual skill changes to improvement-orchestrator.

Mitigation: Review the improvement-orchestrator skill and inspect generated changes before relying on the results.

## Reference(s):

- [State Format](artifact/references/state-format.md)
- [Scheduling Guide](artifact/references/scheduling-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or JSONL state artifact descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update autoloop_state.json and iteration_log.jsonl in a user-selected state directory when executed.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

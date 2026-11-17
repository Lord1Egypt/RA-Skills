## Description:

Monitor early-warning signals of AI-driven white-collar labor displacement and macro-financial spillovers. Use when you need a practical indicator framework, thresholds, alert logic, and concise risk updates for employment, consumption, and credit stress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:


## Use Case:

Risk analysts, portfolio managers, and strategy teams use this skill to produce concise monitoring updates on AI-led labor substitution, re-absorption signals, and downstream employment, consumption, and credit stress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for investment or risk decisions rather than advisory monitoring.

Mitigation: Treat generated monitors as advisory, verify underlying data sources and thresholds, and apply human review before portfolio or risk actions.

Risk: Missing, stale, or mixed-frequency indicators can reduce confidence in the composite risk light.

Mitigation: Timestamp each metric, list missing inputs under Data Gaps, and downgrade confidence when coverage is partial.

## Reference(s):

- [AI Displacement Early-Warning Thresholds](references/thresholds.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk monitor, with optional JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a signal board, composite risk light, actionable notes, data gaps, timestamps, and confidence handling.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

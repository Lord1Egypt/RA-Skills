## Description:

Data Analysis Skills helps an agent analyze tabular, CSV, Excel, and pasted data by identifying objects, fields, relationships, data quality issues, evidence-backed findings, security sensitivity, and practical next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renshengruozhiruchujian-sudo](https://clawhub.ai/user/renshengruozhiruchujian-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, operators, and developers use this skill when they need an agent to inspect business tables, compare related datasets, check calculations and relationships, identify data quality problems, and produce evidence-backed action guidance. It is especially suited to spreadsheet-style review where the user wants a careful explanation of what the data supports and what remains uncertain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for detailed spreadsheet relationship analysis and may process sensitive personal, payroll, finance, compliance, or internal business data.

Mitigation: Redact or minimize sensitive fields before use, share only the columns needed for the task, and avoid submitting regulated or confidential data unless the deployment environment is approved for that data.

Risk: Detailed evidence summaries can expose more source data than a user intended to share onward.

Mitigation: Ask for concise evidence summaries and row or column references instead of full reasoning when handling sensitive datasets.

Risk: Spreadsheet conclusions can be misleading if source tables are incomplete, malformed, stale, or ambiguous.

Mitigation: Confirm data scope and freshness, preserve row-level evidence for key claims, and require clarification when relationship keys, units, or field meanings are unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/renshengruozhiruchujian-sudo/skills/data-analysis-skills)
- [Methodology Reference](artifact/REFERENCE.md)
- [Examples](artifact/EXAMPLES.md)
- [Role Perspective Dictionary](artifact/ROLES.md)
- [Evaluation Suite](artifact/evals/evals.json)
- [Trigger Evaluation Suite](artifact/evals/trigger_evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis report with tables, evidence anchors, calculation checks, action recommendations, and security notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depth varies by data complexity; reports may include concise findings, structured phase summaries, relationship tables, confidence labels, and data sensitivity markings.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

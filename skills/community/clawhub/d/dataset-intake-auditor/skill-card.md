## Description:

Checks fields, units, missing-value rates, outliers, and usability before a new dataset is ingested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and dataset owners use this skill to perform a read-only intake check on CSV or TSV datasets before ingestion. It produces a reviewable report covering dataset overview, field summaries, missing values, outliers, unit risks, intake recommendations, and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include sensitive values from local datasets.

Mitigation: Provide only dataset files intended for audit and review or redact Markdown and JSON outputs before sharing.

Risk: Changing spec.json could activate broader directory, pattern, or skill-audit behavior beyond normal CSV or TSV intake checks.

Mitigation: Keep the default csv_audit mode for normal use and review scope before enabling broader inspection modes.

Risk: The report can be mistaken for a formal data-governance decision.

Mitigation: Use it as a reviewable intake draft and confirm final decisions in the official governance process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/dataset-intake-auditor)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Structured Markdown report, or JSON containing the generated report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local CSV/TSV or directory analysis; generated outputs are in Chinese.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Profiles pasted CSV samples to identify columns, missing values, example values, and likely data types before writing transforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to inspect a pasted CSV sample, spot problematic columns, and plan parsing and cleanup before transforming an export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV samples may expose emails, phone numbers, tokens, or sensitive business data.

Mitigation: Share only a small, useful sample and redact sensitive fields before analysis.

Risk: Small samples and complex quoting can lead to incorrect type or column inferences.

Mitigation: Check inferred types against more rows and use a CSV parser for ambiguous quoting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hmahmadcs/skills/csv-schema-profiler)

## Skill Output:

**Output Type(s):** [Markdown, Code]

**Output Format:** [Structured Markdown with an optional Python code sketch]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Column profiles, prioritized cleanup steps, and a short ticket-ready schema summary.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

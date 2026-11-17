## Description:

Retrieves Cargo run results, exports segment or model data to CSV or JSON, and summarizes successes and errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Cargo workspace users use this skill to inspect workflow metrics, retrieve run outputs, export segment or model data, and count successes and errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restarting failed jobs without separate approval can repeat actions or incur charges.

Mitigation: Require separate approval before restarting; check costs and whether earlier steps already changed external systems.

Risk: Exports and signed download URLs may expose workspace or customer data.

Mitigation: Preserve requested export filters, protect downloaded files and signed URLs, and review support-report contents before submission.

Risk: The referenced CLI implementation and sibling safeguards are outside this artifact review.

Mitigation: Pin a reviewed CLI version and keep analytics access read-only where supported.

## Reference(s):

- [Exports and downloads](references/examples/exports.md)
- [Run analytics examples](references/examples/run-analytics.md)
- [Response shapes](references/response-shapes.md)
- [Troubleshooting](references/troubleshooting.md)
- [Cargo skills repository (metadata homepage)](https://github.com/getcargohq/cargo-skills)

## Skill Output:

**Output Type(s):** [Analysis, Text, Files, Shell commands]

**Output Format:** [Text summaries, JSON responses, and CSV or JSON data exports delivered through signed URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports can include workflow run results or filtered segment and model data.]

## Skill Version(s):

1.7.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Audits API documentation, examples, and field definitions for consistency and highlights breaking-change risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and release reviewers use this skill to inspect API documentation directories, OpenAPI text, examples, and field definitions before interface reviews, releases, or integration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local API documentation or directory inputs may contain private or sensitive material that could be sampled into the generated report.

Mitigation: Point the skill at narrowly scoped inputs and redact sensitive material before use when the report may be shared.

Risk: Generated audit findings can be incomplete because the skill samples and structures local text rather than replacing full contract testing.

Mitigation: Treat the output as a review aid and confirm breaking-change decisions against the authoritative API contract and test suite.

Risk: Using --output writes a Markdown or JSON report to the local filesystem.

Mitigation: Choose an intended output path, inspect the generated file before distribution, and use dry-run/stdout behavior when a file is not needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/api-contract-auditor)
- [Artifact README](artifact/README.md)
- [Structured Spec](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Example Output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report by default, with optional JSON output from the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include scan overviews, field consistency risks, example coverage, breaking-change risks, suggested fixes, validation checklists, and items needing confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

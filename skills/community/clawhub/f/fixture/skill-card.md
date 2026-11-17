## Description:

Generate and manage test data fixtures using CLI templates. Use when creating seed data, mock records, or reproducible test datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, seed, validate, import, export, and reset reproducible test data fixtures for local development and test environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL export can generate unsafe executable SQL from imported or untrusted fixture data.

Mitigation: Review fixture data, field names, and table names before executing SQL output; prefer JSON or CSV export for untrusted imported data.

Risk: Reset behavior can delete stored fixture records, including type-specific records without an additional confirmation prompt.

Mitigation: Back up ~/.fixture before reset operations and review the reset scope before running the command.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with bash command examples and generated JSON, JSONL, CSV, or SQL fixture files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local fixture data under ~/.fixture and can export fixtures to caller-specified files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

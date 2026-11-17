## Description:

Flexible Database De guides an agent and user through designing flexible SQLite-backed database schemas with raw data retention, soft fields, business views, and search considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically oriented users use this skill to have an agent elicit database requirements, choose flexible schema patterns, and draft implementation or validation steps for knowledge bases, API integrations, reports, forms, and heterogeneous data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to create database files, edit scripts, and run local Python commands in a project.

Mitigation: Ask the agent for a plan first, approve writes and commands explicitly, and run the generated commands in a project where these changes are intended.

Risk: The package text refers to script and reference templates that are not included in the artifact.

Mitigation: Review any generated replacement scripts carefully and validate database behavior with a small test dataset before using it on important data.

Risk: The security evidence marks the release suspicious because execution and project modification are loosely scoped.

Mitigation: Install only after review, limit filesystem and shell permissions where possible, and verify that outputs do not expose sensitive data or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/db-schema-designer)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, Python, and shell command snippets when implementation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file edits and command execution for database setup; generated scripts should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

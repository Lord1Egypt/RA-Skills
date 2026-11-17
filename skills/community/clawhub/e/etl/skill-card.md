## Description:

Build ETL pipelines with data ingestion, cleaning, and validation steps. Use when ingesting sources, transforming formats, validating data, or scheduling loads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to record ETL pipeline activity, validation notes, schema changes, profiling results, and exports in local plaintext logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user-entered ETL activity notes in local plaintext logs.

Mitigation: Do not log passwords, API keys, private connection strings, raw sensitive records, or confidential production SQL; review permissions on ~/.local/share/etl/ on shared or backed-up machines.

Risk: The skill is an ETL activity logger, not an ETL executor.

Mitigation: Use it to document pipeline steps and validation results; verify actual data movement, transformations, and loads through the systems that perform those operations.

## Reference(s):

- [ClawHub Etl skill page](https://clawhub.ai/bytesagain-lab/skills/etl)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create plaintext activity log and export files under ~/.local/share/etl/ when commands are run.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

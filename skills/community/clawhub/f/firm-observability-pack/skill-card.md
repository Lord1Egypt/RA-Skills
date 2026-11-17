## Description:

Observability pipeline and CI audit pack for JSONL-to-SQLite trace ingestion and CI workflow validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations engineers use this skill to ingest JSONL traces into SQLite for analysis and check CI workflow configurations for security gates and test steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace ingestion may store sensitive operational trace data in a SQLite database.

Mitigation: Confirm trust in the required mcp-openclaw-extensions package and review the database write location and access controls before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool invocation examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local trace and CI configuration paths supplied by the user.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

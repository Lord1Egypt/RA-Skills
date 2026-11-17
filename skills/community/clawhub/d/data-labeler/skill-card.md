## Description:

Data Labeler is a local command-line activity logger for data operations that stores user-provided entries under ~/.local/share/data-labeler/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners can use this skill to log, search, summarize, and export local records of data pipeline activities from shell commands. It is best treated as a lightweight local activity tracker, not as Label Studio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is presented as Label Studio but installs a local command-line logger.

Mitigation: Review the skill description and available commands before installation, and treat it only as a local data-operation activity logger.

Risk: User-provided data is stored as plaintext under ~/.local/share/data-labeler/ and can be surfaced by search, recent-history, status, or export commands.

Mitigation: Do not enter sensitive datasets, customer records, credentials, or private prompts unless local plaintext storage is acceptable for the intended environment.

## Reference(s):

- [ClawHub Data Labeler skill page](https://clawhub.ai/xueyetianya/skills/data-labeler)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local text, JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies or API keys; stores local plaintext logs under ~/.local/share/data-labeler/.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

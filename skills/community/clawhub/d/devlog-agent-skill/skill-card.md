## Description:

Allows agents to log, list, search, and manage developer journal entries for projects using dev-log-cli in a structured SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to maintain project journals, record milestones and blockers, and retrieve prior project context through dev-log-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs dev-log-cli from PyPI through pipx, which introduces a user-level external dependency.

Mitigation: Review or pin the dev-log-cli package before running setup.sh in sensitive environments.

Risk: Developer journal entries are stored persistently and may include project details.

Mitigation: Keep secrets, tokens, customer information, and highly sensitive internal notes out of log entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crimsondevil333333/skills/devlog-agent-skill)
- [dev-log-cli GitHub repository](https://github.com/CrimsonDevil333333/dev-log-cli)
- [dev-log-cli PyPI package](https://pypi.org/project/dev-log-cli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local devlog CLI commands to create, list, search, view, edit, and summarize persistent project log entries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

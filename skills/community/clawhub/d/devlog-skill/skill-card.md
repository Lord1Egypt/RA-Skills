## Description:

A standardized journaling skill for OpenClaw agents to track progress, tasks, and project status using dev-log-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw agents use this skill to keep structured development journals, record progress and blockers, and retrieve project context with dev-log-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs unpinned third-party software.

Mitigation: Review the setup script before installing and prefer pinned, verified versions of pipx and dev-log-cli.

Risk: The setup script may alter the user's shell PATH.

Mitigation: Make PATH changes only with explicit user consent and avoid running setup.sh in privileged automation or sensitive environments.

## Reference(s):

- [Devlog Skill on ClawHub](https://clawhub.ai/crimsondevil333333/skills/devlog-skill)
- [dev-log-cli GitHub project](https://github.com/CrimsonDevil333333/dev-log-cli)
- [dev-log-cli on PyPI](https://pypi.org/project/dev-log-cli/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses dev-log-cli to write and query a local SQLite-backed developer log.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

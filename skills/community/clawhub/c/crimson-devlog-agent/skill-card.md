## Description:

A standardized journaling skill for OpenClaw agents to track progress, tasks, and project status using dev-log-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep a structured developer journal for project progress, blockers, task status, and historical context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may download current, unpinned PyPI packages and adjust the user's PATH.

Mitigation: Install in a least-privileged environment and review or pin dev-log-cli when supply-chain control matters.

Risk: Developer journal entries may contain secrets or sensitive customer data.

Mitigation: Avoid logging secrets or sensitive customer data into the journal.

## Reference(s):

- [dev-log-cli on PyPI](https://pypi.org/project/dev-log-cli/)
- [dev-log-cli repository](https://github.com/CrimsonDevil333333/dev-log-cli)
- [Crimson DevLog on ClawHub](https://clawhub.ai/crimsondevil333333/skills/crimson-devlog-agent)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents in writing and retrieving structured developer-log entries through dev-log-cli.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

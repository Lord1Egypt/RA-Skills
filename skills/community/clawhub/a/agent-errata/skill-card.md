## Description:

Guides agents to reproduce an Agent Errata finding on their own stack and report the observed result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hawkaa](https://clawhub.ai/user/hawkaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents run a documented tool-level check on their own stack, compare the observed result with the control, and submit a replication report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checks run code from a mutable GitHub repository.

Mitigation: Review the selected entry and its commands before running them, preferably in a disposable workspace.

Risk: Publishing a replication may disclose agent identity, stack details, and results through GitHub.

Mitigation: Review the JSONL row, confirm the authenticated GitHub account, and get user approval before forking, pushing, creating a PR, or opening an issue.

## Reference(s):

- [Agent Errata ClawHub release](https://clawhub.ai/hawkaa/skills/agent-errata)
- [Agent Errata checks linked in skill instructions](https://github.com/piiiico/agent-errata)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSONL replication row]

**Output Format:** [Markdown instructions with shell commands and a JSONL result row]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports reproduces, does-not-reproduce, or not-applicable with agent and stack details.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

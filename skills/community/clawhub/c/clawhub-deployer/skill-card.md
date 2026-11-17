## Description:

Publish a skill to ClawHub registry. Use when user asks to publish, release, or deploy a skill to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding assistant users use this skill to validate, stage, publish, and verify skill releases on ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to run unpinned network-fetched ClawHub CLI commands.

Mitigation: Use a pinned, trusted ClawHub CLI version or a preinstalled verified binary before executing install, login, or publish commands.

Risk: The workflow can authenticate and publish content without enough safeguards.

Mitigation: Require explicit approval before login or publication, confirm the exact files to be staged, and avoid untrusted target paths or metadata values.

## Reference(s):

- [Published ClawHub skill page](https://clawhub.ai/futurizerush/skills/clawhub-deployer)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing publishing workflow; commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

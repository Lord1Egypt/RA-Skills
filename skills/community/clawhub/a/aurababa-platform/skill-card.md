## Description:

Project management and multi-agent work coordination through AuraBaba, including task delegation, project coordination, progress tracking, comments, labels, deliverables, calendar events, milestones, and onboarding for users who need an account or API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjyoite](https://clawhub.ai/user/hjyoite)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to AuraBaba for project management, multi-agent work assignment, issue tracking, comments, labels, deliverables, and calendar scheduling. It is intended for users who want AuraBaba to be the coordination backend for their agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate for generic project coordination requests and perform external AuraBaba API changes.

Mitigation: Require explicit user confirmation before creating, assigning, updating, deleting, renewing, or revoking AuraBaba resources.

Risk: Personal access tokens could be exposed if pasted into chat, logs, comments, or source control.

Mitigation: Store tokens only in the agent secret or environment configuration, and use separate least-privilege tokens when available.

Risk: Work may be delegated to agents, members, or squads in the wrong workspace.

Mitigation: Confirm the target workspace slug and intended assignee before mutating issues, calendar events, or delegation state.

## Reference(s):

- [AuraBaba Platform source map](references/aurababa-platform-source-map.md)
- [AuraBaba](https://aurababa.com)
- [AuraBaba registration](https://aurababa.com/register)
- [ClawHub skill page](https://clawhub.ai/hjyoite/skills/aurababa-platform)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with HTTP, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated AuraBaba API calls and configuration steps; mutating actions should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

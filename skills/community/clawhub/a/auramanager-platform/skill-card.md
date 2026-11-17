## Description:

AuraBaba Platform helps agents coordinate project work through AuraBaba issues, comments, labels, metadata, agents, squads, and calendar events using authenticated HTTP API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjyoite](https://clawhub.ai/user/hjyoite)

### License/Terms of Use:

MIT-0

## Use Case:

External users and project teams use this skill to let an agent create, assign, track, and update AuraBaba project work, including issue hierarchies, comments, labels, metadata, agent or squad assignments, and calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be triggered broadly for project-management and scheduling requests, even when the user does not explicitly mention AuraBaba.

Mitigation: Install it only in agents that should route project and calendar workflows to AuraBaba, and require confirmation before acting on a workspace.

Risk: A stored personal access token can authorize changes or deletions to external issues, metadata, labels, tokens, and calendar events.

Mitigation: Use a dedicated, revocable, least-privilege token where available, avoid global installation, and require confirmation of the target workspace, operation, and data before mutating resources.

## Reference(s):

- [AuraBaba Platform Skill on ClawHub](https://clawhub.ai/hjyoite/skills/auramanager-platform)
- [AuraBaba](https://aurababa.com)
- [auramanager-platform source map](references/auramanager-platform-source-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a workspace slug and a personal access token stored as AURAMANAGER_TOKEN.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

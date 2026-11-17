## Description:

Create and manage multi-agent teams in OpenClaw with shared workspace, budget governance, and mesh networking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use Agent Hive to add and coordinate multi-agent workspaces, configure spawn permissions, and audit budget governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent shared multi-agent workspaces with broad writable shared state.

Mitigation: Install only when shared OpenClaw workspaces are intended, review filesystem changes before use, and keep shared memory, scripts, and skills under appropriate access control.

Risk: Budget demotion status alone may not revoke spawn permissions.

Mitigation: Pair demotion with OpenClaw authorization updates, gateway restart, and validation before relying on budget status to restrict agent spawning.

Risk: Workspace setup depends on caller-provided agent identifiers and creates files under the OpenClaw workspace.

Mitigation: Use simple trusted agent IDs only and inspect generated workspace paths before running setup scripts.

## Reference(s):

- [Agent Budget Governance Framework](references/governance.md)
- [Heartbeat Budget Audit Snippet](references/heartbeat-snippet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command snippets, plus bundled Python and shell scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filesystem setup steps for shared OpenClaw workspaces and budget files.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

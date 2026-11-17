## Description:

Spin up and manage E2B cloud sandboxes for agent work when an OpenClaw agent needs an isolated remote Linux sandbox instead of the local workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, reconnect to, inspect, run commands in, expose ports for, snapshot, and terminate E2B cloud sandboxes. It supports work that should run in an isolated remote Linux environment rather than directly on the local OpenClaw host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill lets an agent create and control E2B cloud sandboxes.

Mitigation: Use a limited E2B API key and install the skill only where agent-managed cloud sandbox execution is intended.

Risk: Commands can run in remote sandboxes and may receive environment variables or copied task data.

Mitigation: Avoid passing sensitive local data unless required and review commands before use in high-trust workflows.

Risk: The registration helper writes persistent local mcporter configuration.

Mitigation: Review the mcporter config entry before and after registration.

Risk: The skill depends on Node packages for E2B and MCP behavior.

Mitigation: Update or audit dependencies before use in high-trust workflows.

## Reference(s):

- [E2B Notes](references/e2b-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/e2b-sandbox)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash examples and JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tools return text content containing formatted JSON for sandbox operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

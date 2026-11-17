## Description:

Install, configure, and use Corust Agent (corust-agent-acp), an ACP-compatible coding agent for OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenix500526](https://clawhub.ai/user/phoenix500526)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install Corust Agent, configure acpx and OpenClaw to run it, and provide Discord setup guidance for ACP sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unverified remote Corust Agent binary.

Mitigation: Prefer a pinned and verified Corust release before installation.

Risk: The suggested OpenClaw configuration can grant broad automatic permissions.

Mitigation: Avoid approve-all unless the agent and execution environment are fully trusted.

Risk: The Discord setup uses wildcard access for incoming users.

Mitigation: Replace the wildcard with explicit trusted users, roles, channels, or guilds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phoenix500526/skills/corust-agent)
- [Corust Agent release download](https://github.com/Corust-ai/corust-agent-release/releases/latest/download/agent-darwin-arm64.tar.gz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent should merge configuration into existing acpx and OpenClaw files and present Discord setup commands as instructions rather than running them automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

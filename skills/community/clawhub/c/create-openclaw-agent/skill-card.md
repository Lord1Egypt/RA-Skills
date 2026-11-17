## Description:

Create Agent helps OpenClaw users create configured agents with identity files, team integration, model selection, and communication channel settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengwuzhi](https://clawhub.ai/user/mengwuzhi)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to create new OpenClaw agents, configure role, model, and channel defaults, and update local team and configuration files through either an interactive wizard or command-line arguments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change OpenClaw agent directories, workspace files, openclaw.json, and TEAM.md.

Mitigation: Run dry-run first, use trusted workspace paths, and review the planned file and configuration changes before executing.

Risk: The included token-copying guidance can expose browser or API credentials.

Mitigation: Use an official scoped token or supported login flow, and keep secrets out of shell history and source control.

Risk: Running the skill with elevated privileges can broaden the impact of local writes.

Mitigation: Run it as a non-root user with least-privilege access to the intended OpenClaw workspace.

## Reference(s):

- [Create Agent on ClawHub](https://clawhub.ai/mengwuzhi/skills/create-openclaw-agent)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown identity and workflow files, JSON configuration updates, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports interactive, command-line, and dry-run modes; writes local OpenClaw agent and workspace files when not run in dry-run mode.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

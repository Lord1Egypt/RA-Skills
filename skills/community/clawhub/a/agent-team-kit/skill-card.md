## Description:

Framework enabling AI agent teams to self-manage work queues, clear roles, continuous discovery, and proactive operation via a heartbeat process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancampbell](https://clawhub.ai/user/ryancampbell)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators of multi-agent workspaces use this skill to install a lightweight operating process for discovery, triage, self-service execution, status tracking, and team health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages approval-free task execution and agent spawning from broad inputs.

Mitigation: Add explicit approval gates for shell commands, deployments, package installs, credential access, public communications, deletion, and externally sourced requests.

Risk: Autonomous agents may modify workspace files or spawn work in environments that are not prepared for that behavior.

Mitigation: Use only in workspaces where autonomous agents are allowed to modify files and spawn work, and monitor backlog, status, and blockers regularly.

Risk: Server-resolved provenance is unavailable for this version.

Mitigation: Verify the repository source and pin a reviewed commit before copying templates or appending heartbeat instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryancampbell/skills/agent-team-kit)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown templates and setup instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces process files for intake, roles, opportunities, backlog, status, and heartbeat-driven team operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

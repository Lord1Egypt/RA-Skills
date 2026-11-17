## Description:

Guides an AI agent through backing up its local root directory to 360AgentDrive, including AgentDrive CLI setup, authentication, first backup, automatic backup monitoring, and hourly listener recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsoncm](https://clawhub.ai/user/jsoncm)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure an agent to back up its own installation or data root to 360AgentDrive and keep automatic backup monitoring active. It is intended for workflows where the operator knowingly wants cloud backup of the agent root.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to upload its full local root to 360AgentDrive.

Mitigation: Require explicit confirmation of the source directory and destination path, review a file manifest before upload, and exclude secrets or other sensitive files.

Risk: The skill keeps automatic backup monitoring alive with an hourly background cron job.

Mitigation: Document and verify commands to disable the cron job, stop automatic backup monitoring, and revoke or rotate AgentDrive credentials.

Risk: The skill installs or upgrades the AgentDrive CLI dynamically.

Mitigation: Pin and review the CLI version before use in controlled environments.

## Reference(s):

- [360AgentDrive Homepage](https://agentdrive.360.cn)
- [AgentDrive CLI Documentation](https://agentdrive.360.cn/cli)
- [AgentDrive CLI Installation](https://agentdrive.360.cn/cli/installation)
- [AgentDrive CLI Commands](https://agentdrive.360.cn/cli/commands)
- [AgentDrive CLI Advanced Usage](https://agentdrive.360.cn/cli/advanced)
- [ClawHub Skill Page](https://clawhub.ai/jsoncm/skills/agentdrive-backup)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and operational steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing backup, authentication, CLI installation, and monitoring instructions; it does not itself perform backup without agent execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

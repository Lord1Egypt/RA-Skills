## Description:

OpenClaw Master Ops helps agents guide OpenClaw setup, gateway administration, security auditing, troubleshooting, channel management, automation, and release-change tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer OpenClaw deployments, diagnose failures, harden configuration, manage channels and agents, and track release changes that may require skill updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose destructive or state-changing OpenClaw administration commands, including reset, repair, session, config, plugin, update, and publish actions.

Mitigation: Require human review before execution, inspect the proposed command and target profile, and back up OpenClaw configuration, credentials, and sessions before repair or reset workflows.

Risk: Secrets, credentials, and session operations may expose or alter sensitive operational state.

Mitigation: Use SecretRef-managed values, redact logs and command output, avoid printing tokens or credential paths, and treat secrets/session commands as manual approval actions.

Risk: Cron automation and release-tracker output could propagate outdated or unreviewed release guidance into operational workflows.

Mitigation: Review release-tracker findings independently before editing or republishing the skill, and keep automated sync jobs limited to reporting unless a human approves changes.

## Reference(s):

- [Release Tracking Workflow](references/release-tracking.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [OpenClaw GitHub Releases API](https://api.github.com/repos/openclaw/openclaw/releases)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands, code blocks, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, command sequences, diagnostic steps, and release tracking guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

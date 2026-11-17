## Description:

Agent Deployment Checklist provides production deployment guidance for AI agent infrastructure on dedicated Mac Mini or Linux server hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment engineers use this skill to plan and review dedicated-hardware deployments for client AI agents, including credentials, security hardening, monitoring, backups, memory scaffolding, and day-one onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified remote installers can execute code that has not been pinned or reviewed.

Mitigation: Replace curl-to-bash installation with pinned, checksummed installers or a reviewed local installation procedure.

Risk: Firewall commands and cron jobs can make persistent changes to client infrastructure.

Mitigation: Require explicit approval before applying sudo firewall changes or installing scheduled jobs, and record the accepted configuration.

Risk: Backups and workspaces can accidentally include client credentials or sensitive data.

Mitigation: Keep credentials out of repository and workspace files, enforce restricted permissions, exclude secrets from backups, and encrypt backup storage.

## Reference(s):

- [Agent Deployment Checklist on ClawHub](https://clawhub.ai/samledger67-dotcom/skills/agent-deployment-checklist)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, templates, and inline shell/code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes layer gates, memory-file templates, starter cron examples, hardware requirements, network allowlists, monitoring cadence, and deployment anti-patterns.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

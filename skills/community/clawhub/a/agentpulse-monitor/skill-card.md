## Description:

AI-powered infrastructure monitoring - thin agent, smart cloud, one-command install, real-time alerts, baseline learning, and auto-remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strouddustinn-bot](https://clawhub.ai/user/strouddustinn-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to install and operate a Linux infrastructure monitoring agent that reports server health, service status, resource usage, and alert data to AgentPulse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and persistence controls are too risky for automatic trust on production servers.

Mitigation: Require a verified release or package, avoid curl-to-bash installation, review cron entries before enabling them, and provide a clear uninstall path.

Risk: Credential handling and transport security need review before the agent is trusted.

Mitigation: Protect and rotate API credentials, avoid storing secrets in broadly readable configuration files, and restore normal TLS certificate validation before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/strouddustinn-bot/skills/agentpulse-monitor)
- [AgentPulse Documentation](https://agentpulse.io/docs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands, configuration snippets, API examples, and Python agent code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux, Python 3.8+, curl or wget, cron, an AgentPulse server ID, and an API key.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

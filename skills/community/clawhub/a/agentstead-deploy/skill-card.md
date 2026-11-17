## Description:

Deploy OpenClaw AI agents to AgentStead cloud hosting and manage them through AgentStead API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusmolt](https://clawhub.ai/user/angusmolt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, configure, start, stop, list, and connect AgentStead-hosted agents. It supports channel setup for Telegram, Discord, WhatsApp, and Slack, and includes subscription actions that can deduct funds from an ASTD wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AgentStead credentials, auth tokens, and messaging bot tokens may be exposed if pasted into shell history, logs, or shared terminals.

Mitigation: Prefer the hidden interactive login prompt, avoid placing secrets in shell commands or exported environment variables, store tokens with owner-only permissions, and rotate secrets after testing.

Risk: Subscription commands can deduct ASTD wallet funds.

Mitigation: Manually confirm agent IDs, plan costs, and user intent before running any subscription command.

Risk: The skill executes shell commands and sends HTTPS requests to AgentStead while managing hosted agents and channels.

Mitigation: Review the generated helper script before execution, use least-privilege bot tokens, and install only when real AgentStead or messaging-service credentials are appropriate for the environment.

## Reference(s):

- [Agentstead Deploy on ClawHub](https://clawhub.ai/angusmolt/skills/agentstead-deploy)
- [AgentStead](https://agentstead.com)
- [AgentStead Signup](https://agentstead.com/signup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and helper script code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide API calls that require AgentStead credentials, bot tokens, and explicit confirmation for wallet-deducting subscription actions.]

## Skill Version(s):

1.4.1 (source: server release metadata and artifact/openclaw.skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

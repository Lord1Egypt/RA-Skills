## Description:

Connect your AI SaaS intelligent agent to any messaging channel via OpenClaw (WhatsApp, Telegram, Slack, Discord, iMessage, and more).

This skill is ready for commercial/non-commercial use.

## Publisher:

[amernet](https://clawhub.ai/user/amernet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to connect an Amernet AI SaaS agent to OpenClaw messaging channels, forward user messages to the SaaS API, reset conversations, check agent status, and route AI Growth Engine AutoPilot requests with confirmation before action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected-channel messages and channel identifiers are sent to the external AI SaaS service.

Mitigation: Use the skill only where administrators intend all connected-channel messages to be processed by the AI SaaS service and make that data flow clear to users.

Risk: The skill requests broad account permissions through the AI SaaS API key.

Mitigation: Prefer a narrowly scoped, revocable API token if the service supports one and rotate or revoke credentials when access is no longer needed.

Risk: A configurable base URL could send messages or credentials to an unintended service.

Mitigation: Lock the base URL to the trusted HTTPS SaaS origin before enabling the skill.

Risk: AutoPilot deploy or pause requests can change business campaigns.

Mitigation: Require role checks and explicit confirmation before forwarding deploy or pause confirmations.

## Reference(s):

- [Amernet AI SaaS portal](https://saas.salesbay.ai)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/amernet/skills/amernet-ai-saas)
- [Publisher profile](https://clawhub.ai/user/amernet)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration]

**Output Format:** [Plain text responses with JSON API requests and shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains per-user conversation context through channel and user identifiers; AutoPilot deploy and pause actions require explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

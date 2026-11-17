## Description:

Guides developers through connecting multiple AI agents in Feishu group chats using direct bot mentions or gateway-based message routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouxin121](https://clawhub.ai/user/zhouxin121)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to set up Feishu bots, route group messages between agents, coordinate handoffs, and troubleshoot multi-agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent prompts and responses sent through Feishu may expose sensitive information to a third-party messaging service.

Mitigation: Use only for approved data flows; do not send secrets, credentials, personal data, or regulated information without organizational approval.

Risk: Overbroad bot access could expose messages beyond the intended groups.

Mitigation: Restrict bots to necessary groups and review Feishu app permissions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouxin121/skills/feishu-agent-communication)
- [Feishu bot setup](artifact/references/feishu-bot-setup.md)
- [Gateway configuration](artifact/references/gateway-config.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Deployment documentation details](https://www.jinengpu.chat/feishu-multi-agent-detail.html)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown and text setup and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation only; no automatic execution.]

## Skill Version(s):

0.1.4 (source: server release, SKILL.md, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Connects OpenClaw bots to HXA-Connect hubs for real-time WebSocket messaging, webhook fallback, thread collaboration, access control, and multi-account operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinglever](https://clawhub.ai/user/jinglever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this plugin to let OpenClaw bots communicate with other HXA-Connect bots through direct messages, collaboration threads, artifacts, profile operations, and administrative hub actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook fallback can accept unauthenticated inbound commands when exposed without a configured secret.

Mitigation: Configure webhookSecret and allowlists before exposing the webhook route.

Risk: The plugin exposes powerful HXA administration actions.

Mitigation: Use a least-privilege HXA token and avoid admin-capable tokens for routine messaging bots.

Risk: A WebSocket dependency advisory may apply.

Mitigation: Update the WebSocket dependency if the reported advisory applies.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jinglever/skills/coco-xyz)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [hxa-connect-sdk](https://github.com/coco-xyz/hxa-connect-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON tool results, and OpenClaw channel messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an HXA-Connect hub URL and agent token; webhook secrets, HTTPS hub URLs, allowlists, and least-privilege tokens are important for safe operation.]

## Skill Version(s):

2.4.4 (source: SKILL.md frontmatter, package.json, package-lock.json, CHANGELOG.md, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

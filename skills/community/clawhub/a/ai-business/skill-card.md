## Description:

Connect AI agents to WLdPass commerce workflows for supplier and buyer discovery, smart matching, demand publishing, messaging, webhook automation, and business intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wld-bot](https://clawhub.ai/user/wld-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to let agents search for suppliers or buyers, publish and manage commercial demand, coordinate messages and subscriptions, register webhooks, and review market intelligence through WLdPass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WLdPass account tokens and the security summary notes insecure token handling.

Mitigation: Set WLDPASS_API_TOKEN through a safer secret mechanism, avoid passing real tokens on the command line, and check permissions on ~/.openclaw/openclaw.json.

Risk: The skill enables broad agent-driven commerce actions including messages, demand publishing, community posts, auto-replies, batch operations, and webhook registration.

Mitigation: Require manual approval before actions that send messages, publish demands, post or reply in communities, enable auto-replies, run batch actions, or register webhooks.

Risk: Webhook automation can send business data to a configured endpoint.

Mitigation: Register only trusted webhook URLs and review expected event types before enabling webhook delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wld-bot/skills/ai-business)
- [WLdPass developer homepage](https://wldpass.com/developers)
- [WLdPass OpenClaw skill manifest](https://wldpass.com/api/v1/openclaw/skill-manifest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl examples, tables, setup guidance, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WLDPASS_API_TOKEN for authenticated WLdPass API actions and may configure local OpenClaw settings.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Agent Shark Mindset helps OpenClaw agents generate market-signal briefs, audience-growth content, Telegram publishing flows, and weekly revenue audit reports for monetized financial-content funnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure autonomous OpenClaw agents that scan public market sources, produce financial signal content, publish Telegram updates, and summarize revenue performance. It is intended for financial-content workflows that require review of channel permissions, claims, and compliance obligations before automated posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous Telegram posting could publish financial signals, VIP upsells, or owner reports without prior human review.

Mitigation: Keep cron posting disabled or route runs through manual review until the operator has checked the exact messages, channel IDs, and bot permissions.

Risk: Financial and promotional claims may create compliance or user-protection issues if unsupported or sent to the wrong audience.

Mitigation: Review compliance requirements, require verifiable data points for claims, and confirm public and VIP channel separation before enabling automated delivery.

Risk: The skill requires Telegram credentials and channel identifiers that could post to unintended destinations if misconfigured.

Mitigation: Use scoped bot permissions, validate PUBLIC_CHANNEL_ID, VIP_CHANNEL_ID, OWNER_CHAT_ID, and test with a private review channel before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/agent-shark-mindset)
- [Publisher profile](https://clawhub.ai/user/georges91560)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Telegram Bot API](https://api.telegram.org)
- [Reddit r/algotrading public JSON](https://www.reddit.com/r/algotrading.json)
- [Reddit r/CryptoCurrency public JSON](https://www.reddit.com/r/CryptoCurrency.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Telegram message text, cron configuration snippets, and JSON log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces market-signal, audience-growth, and revenue-audit artifacts that may be posted or saved by an agent.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

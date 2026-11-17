## Description:

Send automatic Bitcoin price alerts when BTC moves ±3% or crosses key levels, powered by BTC-vision.org live data for Telegram, Discord, and Slack workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation builders use this skill to configure Bitcoin price, threshold, and sentiment alerts. It helps agents draft alert checks, notification templates, and optional hourly scheduling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hourly cron scheduling can create persistent background execution under a user or service account.

Mitigation: Only add the cron schedule when hourly checks are intended, the executing account is known, and removal steps are documented.

Risk: Generated alerts can post price, sentiment, and donation-template content into shared Telegram, Discord, or Slack channels.

Mitigation: Review and edit the alert template before installation, especially for shared channels.

Risk: The skill expects outbound calls to BTC-vision.org for live Bitcoin price and sentiment data.

Mitigation: Confirm the environment permits those requests and that users accept the external data dependency.

## Reference(s):

- [BTC-vision.org](https://btc-vision.org)
- [BTC-vision MCP endpoint](https://btc-vision.org/.netlify/functions/mcp)
- [ClawHub skill page](https://clawhub.ai/welove111/skills/btcvision-alert)
- [ClawHub publisher profile](https://clawhub.ai/user/welove111)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API examples, alert templates, JavaScript condition snippets, and cron command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include notification-channel guidance and optional hourly scheduling instructions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

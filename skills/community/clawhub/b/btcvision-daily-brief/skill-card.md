## Description:

Generates a daily Bitcoin market brief from BTC-vision.org data, including price, Fear and Greed Index, halving countdown, and AI prediction summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to produce recurring Bitcoin market summaries for morning briefings or configured Telegram, Discord, or Slack channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated posting or scheduled runs could publish BTCvision-branded market reports to external channels without adequate user review.

Mitigation: Require manual approval and verify each Telegram, Discord, or Slack channel before enabling posting or cron execution.

Risk: The fixed $350,000 AI target and donation footer may be interpreted as promotional or speculative financial content.

Mitigation: Independently verify, clearly label, or remove promotional and speculative content before distributing the brief.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/welove111/skills/btcvision-daily-brief)
- [BTC-vision.org](https://btc-vision.org)
- [BTC-vision MCP endpoint](https://btc-vision.org/.netlify/functions/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown daily brief with API request examples and scheduling/channel posting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live BTC-vision.org data; no API key is described in the artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

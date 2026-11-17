## Description:

Crypto Price Pro queries real-time and historical cryptocurrency prices, generates trend and comparison charts, creates weekly reports, and can send scheduled email summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cscsxx606](https://clawhub.ai/user/cscsxx606)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve cryptocurrency market prices, generate charts and weekly summaries, and configure email delivery for routine price reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send outbound email using SMTP credentials and may be scheduled to run daily.

Mitigation: Use scoped app passwords, store secrets outside shell startup files, and review scheduled jobs before enabling or deploying the skill.

Risk: The skill depends on external chart packages and cryptocurrency market data services.

Mitigation: Install chart dependencies in an isolated virtual environment with pinned versions, and account for CoinGecko API limits and price-data delay.

## Reference(s):

- [Crypto Price Pro on ClawHub](https://clawhub.ai/cscsxx606/skills/crypto-price-pro)
- [cscsxx606 ClawHub publisher profile](https://clawhub.ai/user/cscsxx606)
- [CoinGecko](https://www.coingecko.com/)
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price)
- [CoinGecko market chart endpoint](https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Command-line text output, generated PNG charts, HTML email content, and Markdown documentation with shell examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CoinGecko API data and optional SMTP environment variables for email delivery.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

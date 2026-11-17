## Description:

Monitors cryptocurrency prices via the CoinGecko API and helps trigger threshold alerts with optional Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongtaop1-sys](https://clawhub.ai/user/yongtaop1-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to check cryptocurrency prices, configure above or below price alerts, and optionally send triggered alerts to Telegram or scheduled monitoring jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Price queries are sent to CoinGecko.

Mitigation: Install and run the skill only where outbound CoinGecko requests are acceptable, and avoid putting sensitive trading context into alert messages.

Risk: Optional Telegram delivery shares alert messages with Telegram.

Mitigation: Configure Telegram delivery only with approved bot tokens and chat IDs, and keep alert text limited to information that is acceptable to send externally.

Risk: The sample cron command writes logs under /tmp and could be run with excessive privileges.

Mitigation: Run scheduled checks as a non-root user and write logs to a private, access-controlled location.

Risk: Percentage-move and configurable file-alert claims are not implemented in the bundled script.

Mitigation: Rely on above and below threshold alerts unless the script is extended and reviewed for those additional behaviors.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yongtaop1-sys/skills/crypto-price-monitor)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yongtaop1-sys)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [CoinGecko Coins List Endpoint](https://api.coingecko.com/api/v3/coins/list?per_page=250)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional external API calls to CoinGecko and optional Telegram alert delivery configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

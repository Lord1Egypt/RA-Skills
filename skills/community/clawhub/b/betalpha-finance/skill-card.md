## Description:

Provides agents with China market data for A-shares, funds, ETFs, ETF/LOF premiums and discounts, minute-level stock data, and real-time news through the Betalpha API after the user configures an API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwwd](https://clawhub.ai/user/lwwd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve China financial market data, including stocks, funds, ETFs, ETF/LOF premium or discount data, minute bars, and news. It is suited for market-data lookup and analysis workflows after the user has configured a Betalpha API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Betalpha API token stored locally, and setup instructions can expose the token if a user pastes it into chat or runs verification commands that print it.

Mitigation: Configure the token manually in the local config file, avoid pasting it into chat, avoid commands that print the token, set restrictive file permissions, and rotate the token if it appears in a transcript or terminal log.

Risk: The skill sends API tokens and financial query parameters to ai.firstindex.cn.

Mitigation: Install only if the user trusts ai.firstindex.cn and is comfortable sending the required token and query data to that service.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lwwd/skills/betalpha-finance)
- [Betalpha API discovery](https://ai.firstindex.cn/api/discovery)
- [Betalpha API token QR code](https://ai.firstindex.cn/qr.jpg)
- [Betalpha privacy policy](https://ai.firstindex.cn/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise text, configuration steps, and occasional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market-data summaries returned from the external Betalpha API; users should treat financial data as informational and not as investment advice.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

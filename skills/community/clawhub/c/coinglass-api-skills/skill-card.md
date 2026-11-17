## Description:

CoinGlass API skill that routes user intent to sub-skills for futures, ETF, options, spot, on-chain, indicator, account, news, and financial-calendar market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coinglass-official](https://clawhub.ai/user/coinglass-official)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to help an agent select the relevant CoinGlass API documentation and form market-data requests for crypto futures, ETFs, options, spot markets, on-chain metrics, indicators, account status, news, and financial-calendar data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CoinGlass API keys can be exposed if copied directly into prompts, generated commands, or files.

Mitigation: Provide the API key through a secure secret mechanism and avoid hardcoding it in prompts or stored artifacts.

Risk: News and article responses may include HTML content from external sources.

Mitigation: Treat returned HTML as untrusted content and render or summarize it as data, not as agent instructions.

Risk: The skill can cause an agent to call external CoinGlass API endpoints.

Mitigation: Install and enable it only when API access to CoinGlass market-data endpoints is intended.

## Reference(s):

- [CoinGlass API SKILL on ClawHub](https://clawhub.ai/coinglass-official/skills/coinglass-api-skills)
- [CoinGlass API skills homepage](https://github.com/coinglass-official/coinglass-api-skills)
- [Root routing table](artifact/SKILL.md)
- [API error codes](artifact/account/references/errors-codes.md)
- [Plans, intervals, and history length](artifact/account/references/plans-interval-history-length.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a CoinGlass API key for endpoint calls.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

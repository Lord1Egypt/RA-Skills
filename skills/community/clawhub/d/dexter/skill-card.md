## Description:

Autonomous financial research agent for stock analysis, financial statements, metrics, prices, SEC filings, and crypto data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorhvr](https://clawhub.ai/user/igorhvr)

### License/Terms of Use:


## Use Case:

Developers and analysts use Dexter to answer financial research questions about stocks, crypto, company fundamentals, filings, estimates, insider trades, news, and market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation runs mutable third-party code from the Dexter repository.

Mitigation: Review before installing, pin the Dexter repository to a trusted commit, use frozen dependency installs where possible, and avoid running setup as root.

Risk: API keys may be stored in plaintext configuration.

Mitigation: Store API keys with restrictive permissions or inject them at runtime, and add .env to ignore rules.

Risk: Confidential research queries may be sent to Tavily when web search fallback is enabled.

Mitigation: Disable or omit Tavily when queries are confidential.

Risk: The skill installs and executes financial research tooling with external API access.

Mitigation: Use a least-privileged or containerized environment and review generated answers before relying on them.

## Reference(s):

- [Dexter skill page](https://clawhub.ai/igorhvr/skills/dexter)
- [Financial Datasets API](https://financialdatasets.ai)
- [Tavily](https://tavily.com)
- [Anthropic Console](https://console.anthropic.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and financial analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use external financial data, web search, and LLM APIs when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

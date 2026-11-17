## Description:

Autonomous financial research agent for stock analysis, financial statements, metrics, prices, SEC filings, and crypto data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to answer financial research questions about public companies, market data, SEC filings, analyst estimates, insider trades, news, and crypto assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation fetches and runs unpinned third-party code.

Mitigation: Pin the Dexter repository to a reviewed commit and use a locked dependency install before deployment.

Risk: API keys are persisted in an environment file.

Mitigation: Protect the .env file with owner-only permissions and avoid storing unnecessary credentials.

Risk: Financial queries and research context may be sent to external services.

Mitigation: Use only non-confidential financial queries and review external service handling requirements before use.

Risk: The skill may produce incorrect or stale financial analysis.

Mitigation: Review outputs against authoritative market, filing, or financial data sources before making decisions.

## Reference(s):

- [abe-dexter ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-dexter)
- [SkillBoss API Hub](https://api.heybossai.com)
- [Financial Datasets](https://financialdatasets.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sourced financial analysis, installation steps, API key configuration guidance, and command-line usage examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

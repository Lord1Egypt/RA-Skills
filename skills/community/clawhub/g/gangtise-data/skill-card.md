## Description:

Retrieves structured quantitative financial data from the Gangtise Open API, including daily K-line market data, financial statements, business composition, shareholder data, earnings forecasts, and valuation percentiles, and saves tabular results for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtisegts](https://clawhub.ai/user/gangtisegts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Gangtise financial APIs for complete security-code-based market, financial statement, business composition, shareholder, earnings forecast, and valuation data. It is intended for workflows that need precise numeric time series or wide tables saved as CSV for downstream analysis or charting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Gangtise requests may be redirected to an environment-controlled server through GANGTISE_DOMAIN.

Mitigation: Remove or tightly control GANGTISE_DOMAIN before use, and prefer a version that validates the shareholder API host before sending the Authorization header.

Risk: The skill requires Gangtise credentials and writes query results plus usage records under workspace/gangtise.

Mitigation: Install only in trusted workspaces, protect GTS_ACCESS_KEY and GTS_SECRET_KEY or scripts/.authorization, and review generated files before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gangtisegts/skills/gangtise-data)
- [Gangtise earning forecast Open API](https://open.gangtise.com/application/open-fundamental/earning_forecast)
- [Earning forecast data guide](references/earning_forecast.md)
- [Financial statement data guide](references/financial.md)
- [Main business data guide](references/main_business.md)
- [Quote data guide](references/quote.md)
- [Shareholder data guide](references/shareholder.md)
- [Valuation data guide](references/valuation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful script runs write CSV query results and usage records under workspace/gangtise.]

## Skill Version(s):

1.4.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Normalized company financial statements and computed ratios from SEC EDGAR via Edgrapi.com for US-listed tickers, including income, balance-sheet, cash-flow, margin, return, leverage, and liquidity data parsed from EDGAR XBRL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research agents use this skill when a user explicitly asks for US-listed company fundamentals or ratios from SEC EDGAR-derived data. It is not intended for live stock prices or incidental ticker mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Edgrapi API key and spends Edgrapi credits on each request.

Mitigation: Install it only for workflows that need Edgrapi fundamentals, set EDGRAPI_KEY deliberately, and monitor credit usage.

Risk: The skill provides filings-derived fundamentals and ratios, not live market prices.

Mitigation: Use a separate market-data source for live prices or price-based ratios.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paperandbeyond23-gif/skills/edgrapi-fundamentals)
- [Server-resolved GitHub provenance](https://github.com/paperandbeyond23-gif/edgrapi-skills/tree/main/skills/edgrapi-fundamentals)
- [Edgrapi homepage](https://edgrapi.com)
- [Edgrapi app](https://edgrapi.com/app)
- [Edgrapi pricing](https://edgrapi.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tool-call descriptions and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EDGRAPI_KEY; each Edgrapi request consumes one credit.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

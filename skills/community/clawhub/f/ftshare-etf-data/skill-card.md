## Description:

Provides A-share ETF data workflows backed by market.ft.tech, including single-ETF details, paginated ETF lists, OHLC and intraday prices, ETF components, pre-market data, PCF lists, PCF downloads, and trade-date lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer A-share ETF market-data questions by selecting the right sub-skill, running the provided Python dispatcher, and presenting returned ETF details, lists, price series, components, pre-market fields, PCF files, or trade dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ETF lookup terms and query parameters are sent to market.ft.tech.

Mitigation: Install and use the skill only when sharing those ETF queries with market.ft.tech is acceptable.

Risk: PCF downloads can overwrite files through symlinks despite local-path containment checks.

Mitigation: Avoid shared or untrusted output directories and do not choose an output filename that already exists or could be a symlink until the download handler is hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-etf-data)
- [ClawHub publisher profile](https://clawhub.ai/user/shawn92)
- [market.ft.tech ETF data service](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and tables based on JSON API responses; PCF downloads may produce XML file content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may execute local Python scripts that call market.ft.tech and may write PCF XML downloads when an output path is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Macro-driven crypto via Gate-Info and Gate-News MCP for analyzing how macro events such as CPI, NFP, Fed decisions, rates, and payrolls relate to crypto calendars, indicators, news, and market snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer macro-to-crypto impact questions by combining economic calendar data, macro indicators, related news, and crypto market snapshots into a structured analysis report. It is intended for data-driven context, not trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake macro-to-crypto analysis for trading advice.

Mitigation: Keep outputs data-driven, avoid buy/sell recommendations, and state that macro impacts on crypto are uncertain and non-deterministic.

Risk: Missing or failed Gate Info or Gate News MCP tools can leave sections incomplete.

Mitigation: Confirm required MCP servers before use, label unavailable dimensions clearly, degrade gracefully on partial failures, and return a concise setup or retry message if all required tools fail.

Risk: Macro event attribution can overstate causality between economic data and crypto price movement.

Mitigation: Frame relationships as correlation rather than causation, compare actual, forecast, and previous values transparently, and include source timing for data points.

## Reference(s):

- [Gate Info Macro Impact Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/skills/gate-info-macroimpact-staging)
- [ClawHub publisher profile](https://clawhub.ai/user/gaixianggeng)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report with tables, links, and concise narrative assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate Info and Gate News MCP results; labels unavailable data and avoids buy/sell recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

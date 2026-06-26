## Description: <br>
Analyzes how macroeconomic events and indicators such as CPI, NFP, Fed decisions, rates, and payrolls may affect crypto markets using Gate Info and Gate News MCP data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect macro calendars, indicators, related news, and crypto market snapshots into a structured impact analysis for assets such as BTC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Gate Info or Gate News MCP servers may be unavailable or untrusted. <br>
Mitigation: Confirm the configured MCP servers are trusted before installation and degrade gracefully when required tools are unavailable. <br>
Risk: Macro-to-crypto analysis can be mistaken for trading advice or deterministic price prediction. <br>
Mitigation: Treat outputs as informational market analysis, avoid buy or sell recommendations, and state that macro impacts on crypto are probabilistic. <br>
Risk: Broad macro questions may be answered in a crypto context by default. <br>
Mitigation: Clarify the requested event, indicator, asset, and time range when the user's intent is ambiguous. <br>


## Reference(s): <br>
- [Gate Info Macro Impact Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured market analysis with calendar, indicator, news, market-correlation, impact-assessment, and risk-factor sections.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

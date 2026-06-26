## Description: <br>
Digital Oracle answers prediction questions by using market trading data across prediction markets, equities, commodities, derivatives, yield curves, currencies, and related financial sources, then cross-validating signals into a structured probability report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[komako-workshop](https://clawhub.ai/user/komako-workshop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer market-priced probability questions about macro events, assets, industries, and geopolitical risk. It guides an agent through selecting independent trading signals, fetching public financial data, and producing structured probability estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound requests to public financial APIs, DuckDuckGo, and web pages can reveal the topic of the user's question. <br>
Mitigation: Use the skill only for topics where that network exposure is acceptable, and avoid confidential research topics. <br>
Risk: Snapshot recording can retain sensitive queries or fetched financial data if enabled. <br>
Mitigation: Enable snapshots only in a controlled directory and clean up recorded data after use. <br>
Risk: The Stooq provider can be mistaken for Yahoo Finance provenance because it acts as a compatibility wrapper. <br>
Mitigation: Treat Stooq-backed results as Stooq-sourced when reviewing data provenance. <br>


## Reference(s): <br>
- [Digital Oracle ClawHub Page](https://clawhub.ai/komako-workshop/digital-oracle) <br>
- [Komako Publisher Profile](https://clawhub.ai/user/komako-workshop) <br>
- [Provider API Reference](artifact/references/providers.md) <br>
- [Trading Symbols Directory](artifact/references/symbols.md) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Structured Markdown probability report with signal tables, contradiction analysis, scenario estimates, and concise reasoning.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python provider calls and command examples for fetching public market data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

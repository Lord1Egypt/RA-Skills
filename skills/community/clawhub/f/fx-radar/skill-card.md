## Description: <br>
Fx Radar monitors major foreign exchange rates and helps users query USD, CNY, HKD, JPY, EUR, GBP, USD/CNY, USD/CNH, and related FX movements using public finance data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to retrieve current exchange-rate snapshots and receive lightweight interpretive context for common currency pairs. It is best suited for informational FX monitoring, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound network requests to Yahoo Finance and frankfurter.app for exchange-rate data. <br>
Mitigation: Use it only in environments where those public data-source requests are allowed, or apply a network allowlist before deployment. <br>
Risk: Exchange-rate commentary can be incomplete, stale, or unsuitable for financial decisions. <br>
Mitigation: Treat the output as informational and verify market data and decisions with authoritative financial sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gold3bear/fx-radar) <br>
- [Yahoo Finance chart data endpoint](https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d) <br>
- [Frankfurter foreign exchange API](https://api.frankfurter.app/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with exchange-rate tables and brief commentary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses outbound requests to public exchange-rate data providers; no API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

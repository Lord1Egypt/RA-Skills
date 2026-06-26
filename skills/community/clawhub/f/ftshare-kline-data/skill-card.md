## Description: <br>
FTShare Kline Data queries A-share OHLC K-line data and one-minute intraday price data from market.ft.tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer A-share stock questions that need historical daily, weekly, monthly, or yearly OHLC K-line data, moving averages, volume, turnover, or one-minute intraday prices. It is intended for lookup and presentation workflows that can run Python commands and consume JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock codes and requested time ranges are sent to market.ft.tech. <br>
Mitigation: Avoid sending confidential watchlists, private research context, or sensitive customer-linked queries through the skill in restricted environments. <br>
Risk: Market data can be delayed, unavailable, incomplete, or unsuitable as the only source for financial decisions. <br>
Mitigation: Verify important prices, volumes, and derived conclusions against authoritative market data before making trading, compliance, or customer-facing decisions. <br>
Risk: The skill is limited to documented A-share stock code formats and specific K-line or intraday endpoints. <br>
Mitigation: Use only supported stock identifiers and query parameters, and choose another data source for unsupported markets, adjustment methods, or broader financial analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shawn92/ftshare-kline-data) <br>
- [market.ft.tech API base](https://market.ft.tech/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, json, guidance] <br>
**Output Format:** [JSON from Python command output, typically summarized for users as Markdown tables or bullet points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include OHLC values, volume, turnover, MA5/MA10/MA20, previous close, current trading day, and Beijing-time timestamps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

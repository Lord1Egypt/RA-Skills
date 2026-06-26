## Description: <br>
Provides A-share ETF market-data lookups from market.ft.tech, including ETF details, paginated lists, OHLC history, intraday prices, PCF lists and downloads, holdings, pre-market data, and trading-day lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer ETF market-data questions by routing requests to the appropriate ETF lookup handler and presenting returned data as JSON, tables, or concise summaries. It is suited for ETF quotes, lists, OHLC history, intraday prices, PCF files, holdings, pre-market data, and recent trading-day workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ETF query details are sent to market.ft.tech. <br>
Mitigation: Use the skill only when sharing the requested ETF symbols, dates, filters, and query details with market.ft.tech is acceptable. <br>
Risk: The PCF download workflow can write an XML file using a user-selected output filename. <br>
Mitigation: Choose output filenames deliberately and avoid paths that could overwrite files in the allowed working directory. <br>
Risk: The skill runs bundled Python handlers to make network requests and process responses. <br>
Mitigation: Review and scan the skill before deployment, and run it in the normal agent sandbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shawn92/ftshare-etf-data) <br>
- [Publisher profile](https://clawhub.ai/user/Shawn92) <br>
- [market.ft.tech data service](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [JSON from handlers with human-facing markdown or table summaries; PCF downloads are XML files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact market.ft.tech and may write a PCF XML file when the user requests a download.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

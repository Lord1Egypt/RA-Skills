## Description: <br>
使用东方财富 API 获取沪深 A 股及指数的日内分时行情，并按表格整理价格、成交量、成交额和均价。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bensema](https://clawhub.ai/user/bensema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer user questions about Shanghai and Shenzhen A-share or major index intraday prices by resolving the secid, querying Eastmoney, and formatting the returned time-series data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock or index identifiers requested by the user may be sent to Eastmoney through an HTTPS request. <br>
Mitigation: Verify the ticker or secid before querying and avoid treating queried identifiers as private. <br>
Risk: Returned intraday prices can be stale, unavailable, or from the previous trading day, and broad trigger wording may invoke the skill for general market questions. <br>
Mitigation: Check the response status and data fields, describe the source and timing limits, and treat returned prices as informational. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bensema/dfcf-stock-intraday) <br>
- [Eastmoney trends2 API endpoint](https://push2.eastmoney.com/api/qt/stock/trends2/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with tabular intraday market data and an optional curl command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Makes an HTTPS request to Eastmoney; returned prices are informational and may reflect the previous trading day outside trading hours.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Provides A-share index data from market.ft.tech, including single-index details, paginated index lists with sorting and filtering, OHLC candles, minute-level intraday prices, and recent trading-date lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and summarize A-share index market data, including index details, lists, K-line history, intraday prices, and trading-date offsets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to market.ft.tech and returns third-party market data. <br>
Mitigation: Install only if those outbound requests are acceptable, and present returned data as third-party market data rather than verified financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shawn92/ftshare-index-data) <br>
- [market.ft.tech API](https://market.ft.tech) <br>
- [Index Description API](https://market.ft.tech/data/api/v1/market/data/index-description-all) <br>
- [Index Detail API Example](https://market.ft.tech/app/api/v2/indices/000001.XSHG) <br>
- [Index OHLC API Example](https://market.ft.tech/app/api/v2/indices/000001.XSHG/ohlcs?span=DAY1&limit=50) <br>
- [Index Intraday Prices API Example](https://market.ft.tech/app/api/v2/indices/000001.XSHG/prices?since=TODAY) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only outbound HTTPS requests to market.ft.tech; returned market data should be treated as third-party data rather than verified financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

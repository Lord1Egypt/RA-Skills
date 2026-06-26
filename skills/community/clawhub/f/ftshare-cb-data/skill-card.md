## Description: <br>
A Share convertible bond data skill set for market.ft.tech that covers full convertible bond lists, single-bond base data, and historical candlestick data for supported convertible bonds and A shares. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query A Share convertible bond lists, bond details such as conversion price and maturity date, historical candlestick data, and prior trading dates through market.ft.tech data endpoints. Results should be used as informational market data, not trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Python scripts send market-data queries to market.ft.tech. <br>
Mitigation: Install and run the skill only in environments where outbound requests to market.ft.tech are acceptable, and review bundled scripts before deployment. <br>
Risk: Returned market data can be incomplete, delayed, or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as informational and verify important financial data with authoritative sources before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shawn92/ftshare-cb-data) <br>
- [market.ft.tech](https://market.ft.tech) <br>
- [Convertible bond base data endpoint](https://market.ft.tech/data/api/v1/market/data/cb/cb-base-data?symbol_code=110070.SH) <br>
- [Stock and convertible bond candlesticks endpoint](https://market.ft.tech/data/api/v1/market/data/stock-candlesticks) <br>
- [Convertible bond list endpoint](https://market.ft.tech/data/api/v1/market/data/cb/cb-lists) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON responses with optional Markdown tables or bullet summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python scripts call market.ft.tech endpoints and print JSON to standard output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

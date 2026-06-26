## Description: <br>
Fetches China A-share market data, including K-line bars, real-time quotes, and tick-by-tick transactions, through the mootdx/TDX protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangdinglu](https://clawhub.ai/user/wangdinglu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to integrate China A-share market data into analysis, data retrieval, and trading-data workflows. It is most useful when code needs examples or setup guidance for mootdx, TDX quote APIs, intraday bars, batch quotes, or transaction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The mootdx/tdxpy trading-hour bypass can produce empty, stale, or unexpected data outside normal market conditions. <br>
Mitigation: Validate returned timestamps and trading calendars before using results in financial automation. <br>
Risk: The skill depends on runtime installation of mootdx and its transitive dependencies. <br>
Mitigation: Use an isolated Python environment and pin or review dependency versions before deployment. <br>


## Reference(s): <br>
- [API Reference](api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangdinglu/a-share-real-time-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API usage examples, setup commands, stock-code formatting guidance, trading-calendar caveats, and risk notes for real-time or historical market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Fetch China A-share stock market data (bars, realtime quotes, tick-by-tick transactions) via mootdx/TDX protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangdinglu](https://clawhub.ai/user/wangdinglu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and market-data analysts use this skill to generate guidance, code examples, shell commands, and configuration steps for retrieving China A-share bars, quotes, and tick-by-tick transaction data with mootdx/TDX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can install Python packages into the active environment. <br>
Mitigation: Run setup and verification in a virtual environment or disposable agent runtime before using it in a shared environment. <br>
Risk: The skill depends on outbound connectivity to third-party TDX market-data servers. <br>
Mitigation: Use only in environments where this network access is allowed, and handle empty or unavailable responses as normal data-quality conditions. <br>
Risk: The trading-hour bypass can produce data outside mootdx's built-in trading-time checks. <br>
Mitigation: Treat returned data as market-data assistance, validate trading days and timestamps, and avoid relying on it as a guarantee for trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangdinglu/free-a-share-real-time-data) <br>
- [Mootdx API Reference](api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market-data caveats for trading hours, stock-code formats, unsupported Beijing Stock Exchange symbols, and network connectivity to third-party TDX servers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

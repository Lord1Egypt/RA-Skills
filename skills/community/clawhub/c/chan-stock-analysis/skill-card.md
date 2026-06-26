## Description: <br>
Provides multi-timeframe Chan theory stock, index, and XAUUSD market analysis using BARF/CZSC methods, real-time market data fallbacks, and optional chart generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyuzhy](https://clawhub.ai/user/zhouyuzhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze A-share, Hong Kong, U.S. equity, index, and XAUUSD price action across daily, 30-minute, 5-minute, and 1-minute timeframes. It produces structured Chan theory analysis, scenario classifications, trading posture guidance, and optional visual charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save analysis outputs to local knowledge-base folders and upload reports or charts to Baidu Cloud when bypy is configured. <br>
Mitigation: Review or disable bypy upload/download behavior before use, and set local Obsidian paths deliberately. <br>
Risk: Financial-analysis output may be interpreted as trading advice or may rely on incomplete or stale market data. <br>
Mitigation: Treat generated analysis as informational, verify source data independently, and require human review before making investment decisions. <br>
Risk: The skill references external data APIs and dependencies that may require credentials or unpinned installation. <br>
Mitigation: Provide credentials through environment variables, remove unwanted defaults, and pin or pre-review dependencies before deployment. <br>


## Reference(s): <br>
- [CZSC framework](https://github.com/waditu/czsc) <br>
- [itick.org forex kline API](https://api.itick.org/forex/kline) <br>
- [ClawHub skill page](https://clawhub.ai/zhouyuzhy/chan-stock-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/zhouyuzhy) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis reports with optional PNG chart files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved to a configured local Obsidian stock directory and uploaded to Baidu Cloud when bypy is configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

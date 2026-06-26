## Description: <br>
One-click deployment guidance for a Freqtrade quantitative trading bot, including dependency installation, spot-trading configuration, strategy setup, and WebUI monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namogu](https://clawhub.ai/user/namogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and configure a Freqtrade trading bot, connect exchange API keys, launch trading, and monitor activity through the WebUI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trading bot deployment can expose the WebUI control interface and make live trading with real funds easy to start. <br>
Mitigation: Review carefully before installing, start with dry-run or paper trading, set small stake limits, bind the WebUI to localhost or firewall it, and replace all WebUI/API secrets. <br>
Risk: Exchange API keys can authorize real trades if permissions are broad or credentials are reused. <br>
Mitigation: Use restricted exchange API keys with withdrawals disabled, enable IP allowlists where available, and keep API secrets out of shared files and logs. <br>
Risk: Mutable remote installer commands can change behavior over time. <br>
Mitigation: Review the installer before execution or pin the fetched code to a trusted version. <br>


## Reference(s): <br>
- [Freqtrade official documentation](https://www.freqtrade.io) <br>
- [Freqtrade Chinese documentation](https://www.itrade.icu/zh/freqtrade/freqtrade) <br>
- [Freqtrade strategy customization](https://www.freqtrade.io/en/stable/strategy-customization/) <br>
- [Freqtrade repository](https://github.com/freqtrade/freqtrade) <br>
- [Detailed usage guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment steps, Freqtrade configuration snippets, WebUI access details, and operational commands.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

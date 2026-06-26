## Description: <br>
Crypto Market Analysis fetches public Binance market data, calculates common technical indicators, and prepares structured cryptocurrency market analysis prompts and reports for an agent-connected LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LunaWolves07](https://clawhub.ai/user/LunaWolves07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to gather Binance price and kline data, compute technical indicators, and generate structured cryptocurrency market analysis reports. It is intended for informational market analysis and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically install an unpinned TA-Lib package into a hard-coded Anaconda Python environment. <br>
Mitigation: Review before installing; preinstall a pinned TA-Lib dependency in an isolated environment and disable runtime package installation. <br>
Risk: The skill can alter the local Python subprocess environment while running indicator calculations. <br>
Mitigation: Run it in a disposable or isolated Python environment and review environment changes before using it in a managed workspace. <br>
Risk: Cryptocurrency analysis output can be mistaken for trading advice. <br>
Mitigation: Present generated reports as informational analysis only and require human review before any financial decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LunaWolves07/crypto-market-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/LunaWolves07) <br>
- [Binance API notes](references/binance_api_notes.md) <br>
- [Technical indicators](references/technical_indicators.md) <br>
- [Binance klines API](https://api.binance.com/api/v3/klines) <br>
- [Binance 24hr ticker API](https://api.binance.com/api/v3/ticker/24hr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON containing market data and an LLM prompt, with expected Markdown report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Binance REST API responses and technical indicator calculations for the requested symbol and intervals.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Provides real-time cryptocurrency prices, market scans, and technical indicators such as RSI, MACD, Bollinger Bands, EMA, and SMA using public market-data APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve public cryptocurrency market data, monitor common trading pairs, and calculate technical indicators for technical reference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local shell script that makes public market-data requests to Binance and CoinGecko. <br>
Mitigation: Install only when that network behavior is acceptable, and review the script before use. <br>
Risk: A user-controlled pairs filter can be inserted into Python code. <br>
Mitigation: Do not let untrusted prompts supply arbitrary command arguments until the pair-filter input handling is fixed. <br>
Risk: The security summary says the documentation under-discloses some behavior. <br>
Mitigation: Review behavior against the artifact before deployment, and do not provide wallet secrets, exchange credentials, or private financial data. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/bytesagain-crypto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text tables and short numeric indicator summaries, with shell command examples when invoked by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Binance and CoinGecko market-data APIs; no API key is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

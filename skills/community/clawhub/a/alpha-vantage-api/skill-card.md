## Description: <br>
Alpha Vantage API helps agents look up stock quotes, daily, weekly, and monthly market history, foreign exchange rates, and cryptocurrency exchange rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kpaxqin](https://clawhub.ai/user/kpaxqin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve financial market data from Alpha Vantage for stocks, forex pairs, and cryptocurrency pairs. It supports quick quote checks, recent historical K-line data, and API-key configuration for higher request limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested symbols or currency pairs, and the configured API key, to Alpha Vantage. <br>
Mitigation: Use only symbols or pairs you are comfortable sending to Alpha Vantage, and review Alpha Vantage terms and privacy expectations before use. <br>
Risk: The apikey command stores the API key in a local config.json file beside the script. <br>
Mitigation: Avoid setting keys in shared or logged terminals, protect the generated config.json file, and delete it when the key is no longer needed. <br>


## Reference(s): <br>
- [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON printed to stdout for data lookup commands; plain text for help, configuration, and errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lookup results depend on Alpha Vantage availability, API limits, and the configured API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

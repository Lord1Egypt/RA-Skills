## Description: <br>
AKShare 开源金融数据接口库 - 支持A股、港股、美股、期货、期权、基金、债券、外汇、宏观数据，免费无需API Key。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to install and call AKShare for public financial market, fund, bond, foreign exchange, and macroeconomic data. It helps agents produce Python examples, data retrieval workflows, and analysis guidance without requiring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Python financial-data packages and may make outbound requests to public market-data providers. <br>
Mitigation: Install only in environments where those dependencies and outbound requests are acceptable; pin dependency versions in sensitive or production environments. <br>
Risk: Retrieved market data and sample screening code can be incomplete, stale, or unsuitable for investment decisions. <br>
Mitigation: Validate returned data before use and do not treat outputs as investment advice. <br>


## Reference(s): <br>
- [ClawHub AKShare skill page](https://clawhub.ai/coderwpf/aakshare) <br>
- [AKShare documentation](https://akshare.akfamily.xyz/) <br>
- [AKShare API reference](https://akshare.akfamily.xyz/data/index.html) <br>
- [AKTools documentation](https://aktools.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pandas DataFrame-oriented examples and data-validation guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

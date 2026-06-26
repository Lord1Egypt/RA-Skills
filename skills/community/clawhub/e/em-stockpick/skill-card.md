## Description: <br>
Uses EastMoney to perform natural-language conditional stock screening across A-shares, Hong Kong stocks, ETFs, convertible bonds, and sectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverfoxchina-gif](https://clawhub.ai/user/silverfoxchina-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to translate natural-language stock-selection criteria into EastMoney queries and collect matching market results. It is intended for screening workflows, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches browser automation and contacts EastMoney services during stock-selection queries. <br>
Mitigation: Run it only in environments where that network and browser activity is expected and allowed. <br>
Risk: The skill writes CSV query results and caches an EastMoney site fingerprint under a local workspace directory. <br>
Mitigation: Review generated files before sharing them and clear the workspace cache when the retained fingerprint is no longer wanted. <br>
Risk: Stock-screening output may be incomplete, stale, or unsuitable for financial decisions. <br>
Mitigation: Treat results as screening data and verify them with authoritative sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silverfoxchina-gif/em-stockpick) <br>
- [EastMoney stock selector](https://xuangu.eastmoney.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Command-line execution with logged status and CSV result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a natural-language query and select type; writes CSV results and a cached EastMoney fingerprint under workspace/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

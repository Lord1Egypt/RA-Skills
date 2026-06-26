## Description: <br>
Provides real-time Chinese A-share, fund, ETF, valuation, news, and market-data queries through the Betalpha finance API after the user configures an API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LWWD](https://clawhub.ai/user/LWWD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to let an agent retrieve Chinese market data, including stocks, funds, ETFs, intraday prices, valuations, and recent finance news. The skill is useful when an agent needs current finance data from Betalpha after an API token has been configured locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Betalpha API token that can be exposed if pasted into chat, printed during verification, shared, or stored with broad file permissions. <br>
Mitigation: Configure the token manually in ~/.config/betalpha/api_key.txt, restrict the file to the current user, avoid printing or sharing the token, and rotate it if exposure is suspected. <br>
Risk: The API token and finance queries are sent to ai.firstindex.cn when the skill retrieves endpoints and market data. <br>
Mitigation: Install only if you trust ai.firstindex.cn with the token and query data, and review the service privacy policy and account controls before use. <br>
Risk: Local credential and endpoint-cache files may persist after the skill is no longer used. <br>
Mitigation: Delete ~/.config/betalpha/ during uninstall or when access is no longer needed. <br>
Risk: Finance data may be delayed, incomplete, or inaccurate and should not be treated as investment advice. <br>
Mitigation: Use the returned data for reference only and verify important decisions against official market or fund sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LWWD/betalpha-finance) <br>
- [Betalpha API discovery endpoint](https://ai.firstindex.cn/api/discovery) <br>
- [Betalpha privacy policy](https://ai.firstindex.cn/privacy) <br>
- [Betalpha token setup QR](https://ai.firstindex.cn/qr.jpg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with finance-query results, setup guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Betalpha API token stored in ~/.config/betalpha/api_key.txt and HTTPS access to ai.firstindex.cn.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

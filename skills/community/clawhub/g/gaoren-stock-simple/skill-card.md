## Description: <br>
股票简单分析 - A股/港股/美股实时行情快速查询 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to query current A-share, Hong Kong, and US stock quotes from stock codes or natural-language stock requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols entered by users are sent to Tencent Finance or Finnhub to retrieve quote data. <br>
Mitigation: Use the skill only when remote quote lookup is acceptable, and avoid entering sensitive watchlists or confidential trading context. <br>
Risk: The artifact includes an embedded Finnhub API token for US stock quote requests. <br>
Mitigation: Prefer a release that moves service credentials into user-controlled configuration before production use. <br>
Risk: Broad natural-language triggers such as stock price questions may activate the skill more often than intended. <br>
Mitigation: Confirm the user wants a remote stock lookup before sending a symbol to an external quote service. <br>
Risk: The Python requests dependency is required but not pinned in the artifact documentation. <br>
Mitigation: Install dependencies in a managed environment and pin or review package versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/gaoren-stock-simple) <br>
- [Publisher profile](https://clawhub.ai/user/gaoren36-arch) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q=) <br>
- [Finnhub quote API](https://finnhub.io/api/v1/quote) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text stock quote summaries and Markdown guidance with example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the requests package; quote freshness and availability depend on Tencent Finance and Finnhub responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

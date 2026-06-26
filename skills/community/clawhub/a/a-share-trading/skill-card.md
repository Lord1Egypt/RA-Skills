## Description: <br>
查询A股实时行情、历史K线、技术指标、个股事件、资金面、A+H双重上市信息、赴港上市节点和行业信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shouldnotappearcalm](https://clawhub.ai/user/shouldnotappearcalm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent developers use this skill to answer A-share market-data questions by running bundled scripts and returning structured summaries. It is suited for quote lookup, historical and technical analysis, stock events, A+H company lists, IPO timeline checks, and industry classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock queries are sent to third-party market-data APIs. <br>
Mitigation: Use the skill only when this data sharing is acceptable for the user and environment. <br>
Risk: Unpinned Python data packages can change behavior over time. <br>
Mitigation: Install in an isolated environment and pin or review dependencies before operational use. <br>
Risk: Financial indicators may be incomplete, delayed, or unsuitable as investment advice. <br>
Mitigation: Treat outputs as informational, verify important results with authoritative sources, and avoid using them as the sole basis for investment decisions. <br>


## Reference(s): <br>
- [A股数据 API 完整参考](references/api-reference.md) <br>
- [ClawHub skill release](https://clawhub.ai/shouldnotappearcalm/a-share-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summaries with inline shell commands and optional JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns concise market-data conclusions with data source and timestamp when available; batch outputs include sample count, success rate, duration, and failed codes.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

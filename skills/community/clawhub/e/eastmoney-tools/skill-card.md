## Description:

东方财富金融数据工具集，集成选股、资讯搜索、行情财务查询三大功能。当用户查询 A股、港股、美股相关数据时使用，包括：条件选股、股票推荐、板块成分股；新闻、公告、研报、政策搜索；实时行情、财务指标、公司信息、资金流向等数据查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Eastmoney financial data for A-share, Hong Kong, and U.S. equities, including stock screening, news and research lookup, market quotes, financial metrics, company information, and capital-flow data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored API keys may be exposed if vault credential files are printed during setup.

Mitigation: Parse credentials locally and avoid displaying API keys in terminal output, logs, or agent responses.

Risk: Raw user queries are sent to an external Eastmoney API service.

Mitigation: Avoid submitting personal, confidential, proprietary, or sensitive investment information unless the user accepts sharing it with that service.

Risk: The security verdict is suspicious due to plaintext credential exposure guidance and external data forwarding.

Mitigation: Review the skill before installation and revise credential handling instructions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torchesfrms/skills/eastmoney-tools)
- [Eastmoney API service endpoint](https://mkapi2.dfcfs.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash curl examples and raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY or locally parsed vault credentials; forwards user queries to the Eastmoney API service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Zenrus MCP Server 是一个提供实时货币汇率和石油价格的服务器，支持多种计算功能，适用于金融分析和自动化工具集成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to retrieve current USD/RUB and EUR/RUB exchange rates, current Brent crude oil prices, and barrel purchase calculations for RUB, USD, or EUR amounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the required API key in a local plaintext .env file.

Mitigation: Use a limited-scope key where possible, avoid shared or untrusted working directories, and rotate the key if the .env file may have been exposed.

Risk: The security summary flags mismatched XiaoBenYang/gaokao backend code that weakens trust in where credentials are sent.

Mitigation: Install and run the skill only after reviewing the publisher and backend relationship and confirming that the XiaoBenYang endpoint is acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/currency-and-oil)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown or plain text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; barrel calculation tools accept a numeric amount.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

基于东方财富权威数据库的金融数据查询工具，支持行情、财务及关联关系数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to query Eastmoney financial data with natural language and turn results into tabular files and concise terminal summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial query text and the MX_APIKEY credential are sent to Eastmoney's documented API.

Mitigation: Use the skill only in trusted environments, keep MX_APIKEY in environment variables, and avoid including unrelated secrets or personal data in query text.

Risk: Generated XLSX files contain externally sourced data.

Mitigation: Treat spreadsheet outputs as untrusted external content and avoid enabling external links or active spreadsheet features unless the source is trusted.

Risk: Broad financial queries can return large result sets that may exceed an agent's useful context window.

Mitigation: Scope queries by entity, metric, and time range before requesting data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqk000/skills/eastmoney-fin-data)
- [Eastmoney Miaoxiang Skill Hub](https://marketing.dfcfs.com/views/finskillshub/indexIoMv0EzE)
- [Eastmoney financial data API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown text, shell commands, API request examples, and generated XLSX, TXT, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY and may write query result files to a local output directory.]

## Skill Version(s):

1.0.5 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

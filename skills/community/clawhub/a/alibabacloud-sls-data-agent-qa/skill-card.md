## Description:

Use the semantic definitions in SLS Source Models or Context Models to identify fields, metrics and business definitions, query and analyze log data, and answer business questions. Not for inspecting or managing models themselves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to query Alibaba Cloud SLS logs through Source Models or Context Models, validate the results, and answer business questions with supporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud queries use permissions to access model definitions and log data.

Mitigation: Use a read-only RAM identity scoped to the models and Logstores being analyzed, and verify any endpoint override before connecting.

Risk: Saved query evidence can contain log data.

Mitigation: Protect saved evidence files and remove them when they are no longer needed.

## Reference(s):

- [Python runtime and endpoint configuration](references/python-runtime.md)
- [Exploring a Source Model](references/source-model.md)
- [Exploring a Context Model](references/context-model.md)
- [Source Model readiness checks](references/source-model-readiness.md)
- [Read-only RAM policies](references/ram-policies.md)
- [SLS SQL function reference](references/sql/functions.md)
- [Cross-Logstore JOIN guidance](references/sql/join.md)
- [SCAN analysis guidance](references/sql/scan.md)
- [Incomplete and inexact query results](references/sql/incomplete.md)
- [Chart delivery guidance](references/chart-delivery.md)
- [Alibaba Cloud SLS model permissions](https://www.alibabacloud.com/help/en/sls/configure-sls-dataagent-permissions)
- [GetLogsV2 authorization](https://help.aliyun.com/en/sls/developer-reference/api-sls-2020-12-30-getlogsv2)
- [SLS RAM action and resource reference](https://help.aliyun.com/en/sls/developer-reference/api-sls-2020-12-30-ram)
- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-sls-data-agent-qa)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, SQL queries, Charts, JSON evidence files]

**Output Format:** [Natural-language findings with Markdown query evidence, tables or charts when suitable, and optional structured evidence files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are based on validated query results; query evidence can include data sources and actual time windows.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

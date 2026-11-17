## Description:

Helps agents manage Alibaba Cloud AnalyticDB for MySQL resources via OpenAPI and SDK workflows, including lifecycle operations, configuration changes, status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover Alibaba Cloud AnalyticDB for MySQL APIs, run SDK or OpenAPI workflows, manage resources, verify operations, and troubleshoot cluster state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating Alibaba Cloud resources can create billable resources or disrupt existing AnalyticDB for MySQL environments.

Mitigation: Use least-privilege Alibaba Cloud credentials and review create, update, modify, or set operations before execution.

Risk: The skill may use cloud credentials and network calls to retrieve API metadata or manage resources.

Mitigation: Prefer environment-provided credentials, confirm region and resource identifiers before mutating operations, and keep generated API metadata under output/aliyun-adb-mysql/.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/cinience/skills/aliyun-adb-mysql)
- [Sources](references/sources.md)
- [Alibaba Cloud OpenAPI product page for AnalyticDB for MySQL](https://api.aliyun.com/product/adb)
- [AnalyticDB for MySQL OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/adb/versions/2021-12-01/api-docs.json)
- [AnalyticDB for MySQL single-API metadata pattern](https://api.aliyun.com/meta/v1/products/adb/versions/2021-12-01/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and Python command examples, plus generated JSON and Markdown API inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts should be saved under output/aliyun-adb-mysql/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

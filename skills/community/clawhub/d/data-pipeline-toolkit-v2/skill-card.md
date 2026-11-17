## Description:

快速构建ETL数据管道 — 提取(APIs/数据库/文件)、转换(清洗/过滤/聚合)、加载(数据仓库)，支持定时调度和监控告警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers, operations teams, and developers use this skill to draft ETL pipeline workflows that extract data from APIs, databases, files, cloud storage, or queues; transform records through cleaning, filtering, aggregation, and joins; and load results into databases, warehouses, files, or APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipeline examples may target real APIs, databases, warehouses, storage buckets, or webhook destinations.

Mitigation: Confirm every data source and destination is approved before using the guidance with real systems.

Risk: Credentials can be exposed if connection strings or tokens are pasted directly into commands or logs.

Mitigation: Use least-privilege credentials from environment variables or a secret manager, and avoid secrets in command history.

Risk: ETL workflows can move PII or business-sensitive records into broader storage or reporting systems.

Mitigation: Apply masking, minimization, and destination controls before processing sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/data-pipeline-toolkit-v2)
- [Publisher profile](https://clawhub.ai/user/yesong-hue)
- [AI智造工坊](http://ai.qnitgroup.com)
- [ShadowAI API](https://referer.shadowai.xyz/r/1056448)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable ETL setup guidance; no bundled executable is included in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

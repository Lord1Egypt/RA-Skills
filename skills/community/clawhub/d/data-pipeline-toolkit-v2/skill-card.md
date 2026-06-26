## Description: <br>
快速构建ETL数据管道 — 提取(APIs/数据库/文件)、转换(清洗/过滤/聚合)、加载(数据仓库)，支持定时调度和监控告警。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers, operations teams, and developers use this skill to plan ETL pipelines that extract data from APIs, databases, files, cloud storage, or queues; transform it through cleaning, filtering, aggregation, and joins; and load it into databases, warehouses, files, or APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pipeline examples may involve credentials, connection strings, or protected data sources. <br>
Mitigation: Keep credentials in protected environment variables or a secret manager, grant least-privilege access, and test with non-sensitive data before production use. <br>
Risk: ETL jobs may process PII or confidential business records and move them to unintended destinations. <br>
Mitigation: Review the data classification, source, transformation, and load target before running or scheduling a pipeline. <br>
Risk: Scheduled jobs and webhook alerts can repeatedly send data or failure details to external destinations. <br>
Mitigation: Schedule jobs only after validation and send webhook or alert notifications only to trusted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yesong-hue/data-pipeline-toolkit-v2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; users provide and validate actual pipeline commands, credentials, schedules, and alert destinations in their environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

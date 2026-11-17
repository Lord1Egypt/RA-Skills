## Description:

Helps developers manage Alibaba Cloud Realtime Compute for Apache Flink SQL, from authoring and validation through deployment, operations, performance analysis, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use the skill to design and validate Flink SQL, manage jobs and related resources on Alibaba Cloud Realtime Compute for Apache Flink, and diagnose runtime or performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A job start could target a deployment other than the one the user confirmed.

Mitigation: Resolve and verify the deployment and workspace immediately before starting; pause if the resolved target differs from the confirmed scope.

Risk: Job data or user comments could be exposed through logs or an external model.

Mitigation: Review log and model destinations, and redact sensitive records or comments before recording or sending them.

Risk: The security review was incomplete and some component analysis was partial.

Mitigation: Review the supplied security guidance and validate the skill's behavior in the intended environment before relying on it for production workflows.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-sql-skill)
- [Flink SQL development guide](references/sql/sql-development.md)
- [Lifecycle and deployment guidance](references/lifecycle.md)
- [Configuration and authentication guidance](references/configuration.md)
- [Performance diagnosis guide](references/diagnosis/README.md)
- [Alibaba Cloud Flink SQL deployment quickstart](https://help.aliyun.com/zh/flink/realtime-flink/getting-started/getting-started-for-a-flink-sql-deployment)
- [Alibaba Cloud supported connectors](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/supported-connectors)

## Skill Output:

**Output Type(s):** [Text, Markdown, SQL code, Shell commands, Configuration guidance, Analysis and troubleshooting guidance]

**Output Format:** [Markdown with SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed SQL, CLI commands, configuration examples, and diagnostic steps; platform operations depend on the user's authorization and confirmed target scope.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

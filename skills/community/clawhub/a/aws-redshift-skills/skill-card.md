## Description: <br>
AWS Redshift interaction skill for managing Redshift Provisioned, Redshift Serverless, and executing SQL queries via the Redshift Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danjin](https://clawhub.ai/user/danjin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and operators use this skill to let an agent manage Amazon Redshift provisioned clusters, Redshift Serverless workgroups and namespaces, snapshots, and SQL execution through the Redshift Data API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Redshift and AWS administrative control. <br>
Mitigation: Use a dedicated least-privilege AWS profile or role scoped to approved clusters, workgroups, namespaces, databases, and S3 prefixes. <br>
Risk: Destructive or high-impact operations can affect data, cost, or availability. <br>
Mitigation: Require human review before delete, restore, resize, pause/resume, COPY, UNLOAD, or non-read-only SQL actions. <br>
Risk: The release has no built-in safety gates for production administration. <br>
Mitigation: Enforce approval, environment separation, and production controls outside the skill before production use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/danjin/aws-redshift-skills) <br>
- [Project homepage](https://github.com/danjin/aws-redshift-skills) <br>
- [Redshift Provisioned Cluster Guide](references/provisioned/cluster_guide.md) <br>
- [Redshift Snapshot Guide](references/provisioned/snapshot_guide.md) <br>
- [Redshift Serverless Workgroup Guide](references/serverless/workgroup_guide.md) <br>
- [Redshift Serverless Namespace Guide](references/serverless/namespace_guide.md) <br>
- [Redshift Data API Query Guide](references/data_api/query_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with command examples, Python snippets, configuration values, and structured AWS operation results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Redshift resource identifiers, query status, paginated result summaries, and S3 COPY/UNLOAD operation details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

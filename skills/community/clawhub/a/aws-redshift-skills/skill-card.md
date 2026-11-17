## Description:

AWS Redshift Skills helps agents manage Redshift Provisioned clusters and snapshots, Redshift Serverless workgroups and namespaces, and SQL execution through the Redshift Data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danjin](https://clawhub.ai/user/danjin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and cloud operators use this skill to manage AWS Redshift resources and run Redshift SQL workflows through an agent interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive or costly Redshift actions, including delete, restore, resize, COPY, UNLOAD, and SQL execution.

Mitigation: Use least-privilege AWS credentials in a non-production or tightly controlled account, and review every high-impact operation before allowing execution.

Risk: Security evidence reports unsafe defaults and input-handling concerns.

Mitigation: Remove the default master password pattern, avoid passing untrusted text into COPY or UNLOAD options, and pin installer and dependency versions before production use.

## Reference(s):

- [Redshift Provisioned Cluster Guide](references/provisioned/cluster_guide.md)
- [Redshift Snapshot Guide](references/provisioned/snapshot_guide.md)
- [Redshift Serverless Workgroup Guide](references/serverless/workgroup_guide.md)
- [Redshift Serverless Namespace Guide](references/serverless/namespace_guide.md)
- [Redshift Data API Query Guide](references/data_api/query_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/danjin/skills/aws-redshift-skills)
- [Project Homepage](https://github.com/danjin/aws-redshift-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command snippets, plus structured AWS operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS credentials and AWS_REGION; operations can affect Redshift clusters, workgroups, namespaces, snapshots, S3 data movement, and SQL execution.]

## Skill Version(s):

0.1.0 (source: release metadata and pyproject.toml; SKILL.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Checks Alibaba Cloud OSS cross-region replication settings without modifying resources and explains configuration-related reasons replication may not start.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect OSS replication rules, permissions, sync options, and related settings when investigating missing or delayed replicas or checking disaster-recovery readiness. It reports findings and suggests manual next steps without changing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud account identity, bucket names, and replication settings may be exposed during inspection.

Mitigation: Grant only least-privilege read-only RAM permissions and limit access to diagnostic reports.

Risk: Target verification can reveal object keys, ETags, and sizes.

Mitigation: Use target verification only when needed and handle object metadata as sensitive.

Risk: Supplying raw cloud access keys or secret keys can expose credentials.

Mitigation: Do not provide raw AccessKey or SecretKey values to the skill; use the configured credential chain.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-crr-config-check)
- [OSS cross-region replication overview](https://help.aliyun.com/zh/oss/user-guide/cross-region-replication-overview/)
- [GetBucketReplication reference](https://help.aliyun.com/zh/oss/developer-reference/getbucketreplication)
- [Data replication troubleshooting](https://help.aliyun.com/zh/oss/user-guide/data-replication-troubleshooting)
- [Replication rules reference](references/replication-rules.md)
- [RAM policies reference](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, evidence-backed findings, input sources, read-only confirmation, and next actions.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Discover and map your cloud architecture automatically. View architecture directories, topology, and resource relationships via Tencent Cloud Smart Advisor API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stinggit](https://clawhub.ai/user/stinggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud architects, and operations engineers use this skill to inspect Tencent Cloud Smart Advisor architecture directories, resource relationships, and Well-Architected evaluation results for the account tied to their configured credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud credentials and includes operations that can create or delete cloud roles or enable Smart Advisor authorization.

Mitigation: Use a tightly scoped subaccount or temporary credentials, review permissions before installation, and require explicit user confirmation before IAM or Advisor authorization changes.

Risk: Generated Tencent Cloud console login URLs can grant access while they remain valid.

Mitigation: Treat generated login URLs as secrets, avoid logging or sharing them, and regenerate links only when needed.

Risk: The artifact includes unrelated batch-publishing materials that are not needed for cloud architecture discovery.

Mitigation: Do not run the publishing scripts for normal skill use; limit execution to the environment check and Tencent Cloud Advisor helper scripts needed for the requested task.

Risk: The artifact recommends storing long-lived Tencent Cloud AK/SK values in shell startup files.

Mitigation: Prefer temporary credentials or a tightly scoped account, and avoid placing long-lived secrets in persistent shell configuration where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stinggit/skills/cloud-architecture-discovery)
- [Tencent Cloud Smart Advisor API Overview](https://cloud.tencent.com/document/product/1264)
- [DescribeArchList API Reference](references/api/DescribeArchList.md)
- [DescribeArch API Reference](references/api/DescribeArch.md)
- [DescribeLastEvaluation API Reference](references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API Reference](references/api/DescribeStrategies.md)
- [CreateAdvisorAuthorization API Reference](references/api/CreateAdvisorAuthorization.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON command results and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Tencent Cloud console login links; those links should be treated as secrets while valid.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides a holistic view of cloud architecture diagrams, directories, and risk assessments across a Tencent Cloud account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stinggit](https://clawhub.ai/user/stinggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Tencent Cloud Smart Advisor architecture diagrams, directory trees, evaluation results, and risk assessment items across an account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for Tencent Cloud AK/SK credentials and can generate console login links.

Mitigation: Use a least-privilege Tencent Cloud sub-account, avoid storing long-lived credentials in shell startup files, and treat generated login links as sensitive credentials.

Risk: The skill includes IAM and account-impacting operations, including role creation, role deletion, and Smart Advisor authorization.

Mitigation: Run role creation, cleanup, and authorization only after explicit user approval and after reviewing the CAM impact.

Risk: The server security verdict is suspicious because the IAM and login-link capabilities are broad for a viewing-oriented tool.

Mitigation: Review the skill carefully before installation and constrain execution to the documented Tencent Cloud domains and required environment variables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stinggit/skills/cloud-architecture-holistic-view)
- [Tencent Cloud](https://cloud.tencent.com)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)
- [Tencent Cloud CAM Role Console](https://console.cloud.tencent.com/cam/role)
- [DescribeArch API Reference](references/api/DescribeArch.md)
- [DescribeArchList API Reference](references/api/DescribeArchList.md)
- [DescribeLastEvaluation API Reference](references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API Reference](references/api/DescribeStrategies.md)
- [CreateAdvisorAuthorization API Reference](references/api/CreateAdvisorAuthorization.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON API summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce sensitive Tencent Cloud console login links that should not be logged, cached, or shared.]

## Skill Version(s):

1.4.0 (source: release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

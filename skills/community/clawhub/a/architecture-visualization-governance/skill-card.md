## Description:

Visualize and govern your cloud architectures. Get architecture assessments, risk heatmaps, and compliance dashboards in one place.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stinggit](https://clawhub.ai/user/stinggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud architects, and operations teams use this skill to query Tencent Cloud Smart Advisor data, review architecture diagrams, inspect Well-Architected evaluations, and surface governance recommendations for the currently authenticated Tencent Cloud account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud AK/SK credentials and may operate with broad cloud authority.

Mitigation: Use a dedicated least-privilege Tencent Cloud sub-account and avoid storing long-lived credentials in shell profiles.

Risk: IAM actions can create, attach policies to, or delete a CAM role.

Mitigation: Require explicit user confirmation before IAM-changing actions, review the role policy scope, and remove the role when it is no longer needed.

Risk: Generated console login links can function as temporary access material.

Mitigation: Generate links only when needed, share them only with authorized users, and avoid exposing full login URLs in logs or transcripts.

Risk: The API wrapper can call Tencent Cloud endpoints using configured credentials.

Mitigation: Review or restrict usage to the Tencent Cloud Advisor endpoints and actions needed for architecture assessment workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stinggit/skills/architecture-visualization-governance)
- [Tencent Cloud Advisor console](https://console.cloud.tencent.com/advisor)
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi)
- [Tencent Cloud CAM roles](https://console.cloud.tencent.com/cam/role)
- [DescribeArch API reference](artifact/references/api/DescribeArch.md)
- [DescribeArchList API reference](artifact/references/api/DescribeArchList.md)
- [DescribeLastEvaluation API reference](artifact/references/api/DescribeLastEvaluation.md)
- [DescribeStrategies API reference](artifact/references/api/DescribeStrategies.md)
- [CreateAdvisorAuthorization API reference](artifact/references/api/CreateAdvisorAuthorization.md)
- [ListDirectoryV2 API reference](artifact/references/api/ListDirectoryV2.md)
- [ListUnorganizedDirectory API reference](artifact/references/api/ListUnorganizedDirectory.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command outputs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud console links and generated temporary login links when the user has configured role access.]

## Skill Version(s):

1.4.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

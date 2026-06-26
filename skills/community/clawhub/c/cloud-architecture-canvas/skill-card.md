## Description: <br>
Cloud Architecture Canvas helps an agent use Tencent Cloud Smart Advisor APIs to inspect architecture directories, architecture diagrams, evaluation results, and risk assessment items, and to open Smart Advisor service access when the user explicitly approves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2513483494](https://clawhub.ai/user/2513483494) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to query Tencent Cloud Smart Advisor data, review architecture diagrams and Well-Architected evaluation results, and generate console links for the current Tencent Cloud account. It is intended for accounts where the user can provide Tencent Cloud credentials and approve any IAM or service-enablement actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tencent Cloud credentials to create or delete IAM roles, attach policies, assume roles, and enable Smart Advisor access. <br>
Mitigation: Use a least-privilege Tencent Cloud subaccount or temporary credentials, and require explicit user approval before any IAM or service-enablement action. <br>
Risk: Generated Tencent Cloud console login URLs can grant sensitive account access while valid. <br>
Mitigation: Treat generated login URLs as sensitive access links, avoid logging or sharing them, and regenerate them only when needed. <br>
Risk: Long-lived Tencent Cloud AK/SK values in shell startup files increase credential exposure if the host or profile is shared. <br>
Mitigation: Prefer temporary credentials or a restricted subaccount, and avoid storing long-lived AK/SK values in shell startup files. <br>
Risk: The security guidance calls out TLS fallback behavior that should be reviewed before use. <br>
Mitigation: Review or patch the TLS fallback before installing or using the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/2513483494/cloud-architecture-canvas) <br>
- [Tencent Cloud Smart Advisor Product Documentation](https://cloud.tencent.com/document/product/1278/109059) <br>
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud Smart Advisor Console](https://console.cloud.tencent.com/advisor) <br>
- [CreateAdvisorAuthorization API Reference](references/api/CreateAdvisorAuthorization.md) <br>
- [DescribeArch API Reference](references/api/DescribeArch.md) <br>
- [DescribeArchList API Reference](references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API Reference](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API Reference](references/api/DescribeStrategies.md) <br>
- [ListDirectoryV2 API Reference](references/api/ListDirectoryV2.md) <br>
- [ListUnorganizedDirectory API Reference](references/api/ListUnorganizedDirectory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Tencent Cloud console login links that should be treated as sensitive access links.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

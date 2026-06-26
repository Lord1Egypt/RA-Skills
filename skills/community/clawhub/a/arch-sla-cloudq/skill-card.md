## Description: <br>
Architecture SLA Tracker by CloudQ helps an agent use Tencent Cloud Smart Advisor to inspect architecture diagrams, directory data, risk strategies, and Well-Architected evaluation results, with optional authorized console access workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2513483494](https://clawhub.ai/user/2513483494) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud engineers, SREs, and developers use this skill to query Tencent Cloud architecture inventories, risk assessment strategies, and recent Well-Architected evaluation results. The skill also guides environment checks, role setup, and user-approved authorization steps needed for Smart Advisor workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use powerful Tencent Cloud credentials and perform account-level actions. <br>
Mitigation: Use a least-privilege subaccount or short-lived credentials, and review requested CAM and Smart Advisor permissions before running setup or authorization commands. <br>
Risk: Role setup and cleanup workflows can create, attach policies to, or delete Tencent Cloud CAM roles. <br>
Mitigation: Run role creation or cloud deletion only after explicit user approval, and verify the target role and attached policies before confirming. <br>
Risk: Generated console login links can grant session access to Tencent Cloud pages. <br>
Mitigation: Treat generated login links as sensitive, avoid sharing them, and regenerate links instead of caching or reusing them. <br>
Risk: Long-lived AK/SK credentials may be exposed if stored broadly in shell startup files. <br>
Mitigation: Avoid storing long-lived credentials in shell profiles when possible; prefer temporary credentials or a constrained environment for this skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/2513483494/arch-sla-cloudq) <br>
- [Tencent Cloud Smart Advisor documentation](https://cloud.tencent.com/document/product/1278/109059) <br>
- [CreateAdvisorAuthorization API reference](artifact/references/api/CreateAdvisorAuthorization.md) <br>
- [DescribeArch API reference](artifact/references/api/DescribeArch.md) <br>
- [DescribeArchList API reference](artifact/references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API reference](artifact/references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API reference](artifact/references/api/DescribeStrategies.md) <br>
- [ListDirectoryV2 API reference](artifact/references/api/ListDirectoryV2.md) <br>
- [ListUnorganizedDirectory API reference](artifact/references/api/ListUnorganizedDirectory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Cloud API result summaries and sensitive console login links that should be handled as session-bearing URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

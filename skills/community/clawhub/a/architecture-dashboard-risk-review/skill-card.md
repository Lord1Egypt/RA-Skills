## Description: <br>
Architecture dashboard with integrated risk review. Monitor architecture health, track risk items, and get Well-Architected scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stinggit](https://clawhub.ai/user/stinggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and architecture reviewers use this skill to query Tencent Cloud Smart Advisor data, inspect architecture diagrams and directories, review Well-Architected scores, and surface risk assessment items for the current Tencent Cloud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes admin-capable Tencent Cloud role changes and Smart Advisor authorization steps. <br>
Mitigation: Review each role creation, role deletion, policy attachment, and advisor authorization step before execution, and prefer least-privilege or short-lived credentials. <br>
Risk: Tencent Cloud credentials and generated console login links can expose privileged account access. <br>
Mitigation: Avoid storing long-lived AK/SK in shell startup files, rotate credentials as needed, and treat generated login links as sensitive session material. <br>
Risk: The artifact includes unrelated bulk-publishing evasion guidance that increases supply-chain review concern. <br>
Mitigation: Review package contents before installation and rely on the Smart Advisor functionality rather than publishing guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stinggit/architecture-dashboard-risk-review) <br>
- [Tencent Cloud console](https://cloud.tencent.com) <br>
- [Tencent Cloud Smart Advisor console](https://console.cloud.tencent.com/advisor) <br>
- [DescribeArch API reference](references/api/DescribeArch.md) <br>
- [DescribeArchList API reference](references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API reference](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API reference](references/api/DescribeStrategies.md) <br>
- [CreateAdvisorAuthorization API reference](references/api/CreateAdvisorAuthorization.md) <br>
- [ListDirectoryV2 API reference](references/api/ListDirectoryV2.md) <br>
- [ListUnorganizedDirectory API reference](references/api/ListUnorganizedDirectory.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Cloud console links and account-scoped architecture or risk data returned by Smart Advisor APIs.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

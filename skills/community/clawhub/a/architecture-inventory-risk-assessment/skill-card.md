## Description: <br>
Inventory your cloud architectures and assess risks. Query architecture blueprints, evaluate Well-Architected scores, and identify governance gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stinggit](https://clawhub.ai/user/stinggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to inspect Tencent Cloud Smart Advisor architecture inventories, risk evaluation items, Well-Architected assessment results, and console links for the currently configured Tencent Cloud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence security verdict is suspicious because the artifact combines real Tencent Cloud Advisor functionality with unrelated bulk-publishing guidance. <br>
Mitigation: Review the artifact before installation, remove unrelated publishing files, and install only when the publisher and intended cloud access are trusted. <br>
Risk: The skill can guide high-impact Tencent Cloud access flows, including console-login generation, CAM role setup, and Advisor authorization. <br>
Mitigation: Require explicit approval for each cloud write action and confirm that the requested action matches the user's Tencent Cloud account and business intent. <br>
Risk: Long-lived Tencent Cloud AK/SK credentials increase exposure if stored or reused broadly. <br>
Mitigation: Prefer scoped or temporary credentials where possible and avoid persisting secrets beyond the user's approved environment configuration. <br>
Risk: The security guidance warns not to use the login or API scripts unless TLS verification is fixed. <br>
Mitigation: Block or review those scripts before use and verify secure TLS handling before allowing API or login-link operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stinggit/architecture-inventory-risk-assessment) <br>
- [Skill Instructions](SKILL.md) <br>
- [Tencent Cloud Advisor API Overview](advisor-2020-07-21/API 概览.md) <br>
- [DescribeArch API Reference](references/api/DescribeArch.md) <br>
- [DescribeArchList API Reference](references/api/DescribeArchList.md) <br>
- [DescribeLastEvaluation API Reference](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API Reference](references/api/DescribeStrategies.md) <br>
- [CreateAdvisorAuthorization API Reference](references/api/CreateAdvisorAuthorization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API results and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and Tencent Cloud credentials; cloud query results are scoped to the configured Tencent Cloud account.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Queries FeatureDB read/write usage data from PAI-FeatureStore for consumption analysis, usage trends, cost estimation, and date-range breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to query historical FeatureDB read/write counts, inspect project or feature view trends, and estimate costs for Alibaba Cloud PAI-FeatureStore usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local Aliyun CLI installation, plugin installation, and plugin updates. <br>
Mitigation: Install only if the user trusts Aliyun CLI and is comfortable with its plugin install and update behavior. <br>
Risk: The skill requires cloud credentials and can expose risk if access keys or profiles are mishandled. <br>
Mitigation: Use a dedicated RAM user or temporary STS credentials with documented read-only PAI-FeatureStore permissions, avoid sharing access keys in chat, shells, or CI logs, and secure local Aliyun credential profiles. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pai-feature-store-featuredb-usage-query) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs and CLI Commands](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Setup Script](https://aliyuncli.alicdn.com/setup.sh) <br>
- [PAI Console](https://pai.console.aliyun.com/) <br>
- [RAM Console](https://ram.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and summarized usage analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Alibaba Cloud queries; requires Aliyun CLI, current plugins, and user-provided region and datasource or workspace identifiers.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

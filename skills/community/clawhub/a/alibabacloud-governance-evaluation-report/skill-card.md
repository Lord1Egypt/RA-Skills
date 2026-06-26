## Description: <br>
Queries Alibaba Cloud Governance Center maturity checks and helps generate structured risk and compliance reports for account governance analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud platform engineers, security teams, and operators use this skill to inspect Alibaba Cloud Governance Center results, drill into risky checks, and get remediation-oriented reports for account governance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials to read Governance Center results, which can expose sensitive account posture if credentials are overprivileged or mishandled. <br>
Mitigation: Use a dedicated read-only RAM policy or temporary role-based credentials, and avoid pasting secrets into chat logs, terminal history, or generated reports. <br>
Risk: Governance and non-compliant resource results may reveal sensitive cloud inventory and compliance details. <br>
Mitigation: Treat outputs as sensitive operational data, share them only with authorized users, and redact resource identifiers before external distribution. <br>
Risk: Aliyun CLI auto-plugin installation changes the local execution environment. <br>
Mitigation: Review the Aliyun auto-plugin setting before use and run the skill in a controlled environment with only the required Governance Center permissions. <br>
Risk: The helper script caches Governance Center metadata locally under the user's home directory. <br>
Mitigation: Clear the local governance metadata cache when working on shared systems or when cached metadata should not persist. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-governance-evaluation-report) <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Overview report format](references/report-format-overview.md) <br>
- [Pillar report format](references/report-format-pillar.md) <br>
- [Detail report format](references/report-format-detail.md) <br>
- [Alibaba Cloud Governance Center documentation](https://help.aliyun.com/zh/governance/) <br>
- [Alibaba Cloud Governance API overview](https://help.aliyun.com/zh/governance/developer-reference/api-governance-2021-01-20-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports in chat, with shell command examples and structured JSON from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI 3.3.0 or later, Governance Center read permissions, and user confirmation before running customizable parameters.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

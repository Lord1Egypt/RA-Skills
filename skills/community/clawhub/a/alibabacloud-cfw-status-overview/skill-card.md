## Description: <br>
Provides an Alibaba Cloud Firewall status overview covering asset management, border firewall switch status, and traffic trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security operators and developers use this skill to run Aliyun CLI Cloud Firewall checks and summarize coverage, firewall switch status, asset exposure, and traffic overview information for an Alibaba Cloud account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs credentialed Aliyun CLI commands against the active Alibaba Cloud account. <br>
Mitigation: Use a least-privilege read-only RAM profile and confirm the active account, profile, and region before use. <br>
Risk: The skill can change local Aliyun CLI behavior by enabling AI-mode and updating plugins. <br>
Mitigation: Review CLI and plugin settings before installation, avoid automatic updates unless trusted, and confirm AI-mode is disabled after interrupted runs. <br>
Risk: The skill requires sensitive cloud credentials to be configured locally. <br>
Mitigation: Never paste credentials into chat or command output, and verify credential status without printing Access Key or secret values. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Cloud Firewall API Analysis](references/api-analysis.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report with inline Aliyun CLI commands and CLI-derived status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI, configured Alibaba Cloud credentials, Cloud Firewall read permissions, and a supported Cloud Firewall region.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

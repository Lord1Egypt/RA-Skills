## Description: <br>
Query and analyze security events and alerts detected by Alibaba Cloud Firewall IPS (Intrusion Prevention System), helping quickly locate threats and provide remediation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operations engineers and cloud administrators use this skill to investigate Alibaba Cloud Firewall IPS alerts, identify attacked assets and attack patterns, check IPS configuration, and produce remediation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Alibaba Cloud profile to read Cloud Firewall security data and requires sensitive cloud credentials. <br>
Mitigation: Use a least-privilege read-only RAM policy or temporary credentials and avoid entering long-lived access keys in command lines. <br>
Risk: The skill changes local Aliyun CLI and plugin settings while presenting its Cloud Firewall activity as read-only. <br>
Mitigation: Review setup commands before installation and verify AI-mode, user-agent, and auto-plugin-install settings after use. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [API Analysis - IPS Alert Event Analysis](references/api-analysis.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies - IPS Alert Event Analysis](references/ram-policies.md) <br>
- [Related APIs - IPS Alert Event Analysis](references/related-apis.md) <br>
- [Verification Method - IPS Alert Event Analysis](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include partial results when individual Alibaba Cloud Firewall API calls fail.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

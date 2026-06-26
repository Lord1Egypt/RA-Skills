## Description: <br>
Query and analyze Alibaba Cloud public network exposure, identify unnecessary exposed assets and ports, assess exposure risks, and generate remediation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and cloud operations teams use this skill to audit Alibaba Cloud Firewall public exposure, exposed ports, new exposures, protected asset status, vulnerability coverage, attack events, and inbound ACL policy coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to query Alibaba Cloud Firewall using the local Aliyun CLI profile, which may expose cloud inventory and security posture data to the running agent. <br>
Mitigation: Use a least-privilege read-only RAM user or role, confirm the active Aliyun CLI profile and region before execution, and avoid sharing raw credentials. <br>
Risk: The skill includes commands for CLI installation, plugin updates, AI-mode, and auto-plugin configuration that can change local CLI state. <br>
Mitigation: Approve installation and plugin-update commands only when intentional, and check Aliyun CLI AI-mode and auto-plugin settings after the skill completes. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Cloud Firewall API Analysis](references/api-analysis.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-cfw-exposure-detection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and summarized Alibaba Cloud Firewall API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Aliyun CLI profile and read-only Cloud Firewall permissions.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

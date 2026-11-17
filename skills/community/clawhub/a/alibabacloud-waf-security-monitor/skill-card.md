## Description: <br>
Performs security inspection and monitoring for Alibaba Cloud WAF 3.0 assets, attack events, traffic anomalies, protection status, certificates, and instance inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security engineers and operators use this skill to inspect Alibaba Cloud WAF 3.0 coverage, attack and traffic signals, certificate status, and configuration risks across the cn-hangzhou and ap-southeast-1 WAF business regions. <br>

### Deployment Geography for Use: <br>
Global, with WAF business-region checks limited to cn-hangzhou and ap-southeast-1. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update the local Aliyun CLI plugin environment before running WAF checks. <br>
Mitigation: Install or update the Aliyun CLI and plugins yourself, or run the skill in a controlled shell environment where plugin changes are acceptable. <br>
Risk: The skill uses an existing Alibaba Cloud credential profile to query WAF assets and events. <br>
Mitigation: Use least-privilege read-only RAM permissions or temporary credentials, configure credentials outside the agent session, and never paste access keys into chat or shell history. <br>
Risk: The workflow aggregates raw WAF inspection output in /tmp/waf_skill_output.log, which may include sensitive asset and security details. <br>
Mitigation: Restrict access to the log while the skill runs, then delete it or move it to protected storage after the report is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-security-monitor) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Report Template](references/report-template.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown inspection report with inline shell commands and structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Aliyun CLI WAF OpenAPI responses, local Python helper scripts, and a shared temporary WAF output log for verification.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Performs security inspection and monitoring for Alibaba Cloud WAF 3.0 assets, attack events, traffic, HTTP status anomalies, protection status, certificates, and instance inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security engineers and operators use this skill to inspect Alibaba Cloud WAF deployments, review asset coverage, query attack and traffic signals, and produce a structured WAF inspection report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires cloud credentials and can expose sensitive WAF security findings through command output or logs. <br>
Mitigation: Use least-privilege read-only RAM permissions, prefer OAuth or short-lived credentials, avoid entering access keys in agent-visible commands, and treat generated inspection output as sensitive. <br>
Risk: The workflow changes local Aliyun CLI plugin and AI-mode settings during execution. <br>
Mitigation: Run it only in an environment where those CLI settings are acceptable, confirm setup changes before use, and disable AI-mode when execution ends. <br>
Risk: The workflow writes WAF inspection output to a predictable temporary log path. <br>
Mitigation: Restrict local file permissions, avoid shared machines for execution, and delete or protect /tmp/waf_skill_output.log after review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-waf-security-monitor) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [API Parameter Reference](references/api-reference.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [WAF Inspection Report Template](references/report-template.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown inspection report with CLI command blocks, verification summaries, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Alibaba Cloud WAF CLI outputs and a local verification script to summarize assets, events, traffic, status codes, protection status, and certificate expiry.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

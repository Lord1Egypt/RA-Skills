## Description: <br>
Alibaba Cloud Cloud Firewall ACL rule read-only diagnostic assistant for diagnosing Internet, NAT Boundary, and VPC Boundary Firewall ACL behavior and providing console configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations and security engineers use this skill to troubleshoot Alibaba Cloud Cloud Firewall ACL rules that are not taking effect, inspect matched rules and traffic logs, and receive read-only diagnosis or console-only configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses default Alibaba Cloud CLI credentials to query firewall rules and logs. <br>
Mitigation: Use a read-only RAM user and confirm the active CLI credential context before running diagnostics. <br>
Risk: The skill's setup steps may change persistent local Alibaba Cloud CLI or plugin state even though the diagnostic workflow is presented as read-only. <br>
Mitigation: Manually review, remove, or explicitly approve steps that enable or disable aliyun AI mode, set global user-agent state, update plugins, or install plugins. <br>


## Reference(s): <br>
- [Cloud Firewall ACL Diagnosis Framework](references/diagnosis.md) <br>
- [Cloud Firewall CLI Command Reference](references/cli_commands.md) <br>
- [Cloud Firewall ACL Configuration Guide](references/configuration_guide.md) <br>
- [Security Rules - Complete Prohibitions](references/security_rules.md) <br>
- [RAM Permissions List](references/ram-policies.md) <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-cfw-acl-diagnosis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sdk-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown text with concise diagnostic reports, CLI query context, and console-only remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow; diagnosis reports are constrained to a short fixed structure and should be based on successful CLI query output.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

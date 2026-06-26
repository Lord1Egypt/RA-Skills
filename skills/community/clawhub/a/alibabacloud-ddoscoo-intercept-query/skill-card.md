## Description: <br>
Query Alibaba Cloud DDoS Pro (ddoscoo) block and intercept reasons via SLS full logs and ddoscoo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations and security engineers use this skill to investigate DDoS Pro block reports, query SLS logs by request ID, identify the blocking rule, and produce remediation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects Alibaba Cloud DDoS and SLS data and depends on sensitive Alibaba Cloud credentials. <br>
Mitigation: Use least-privilege, preferably temporary credentials, and do not paste real access keys into command-line examples. <br>
Risk: The workflow can affect live DDoS protection settings, including enable, disable, modify, config, or overwrite operations. <br>
Mitigation: Require explicit human approval, confirm all parameters, and understand rollback impact before running any setting-changing command. <br>
Risk: DDoS full logs can include client IPs, cookies, authorization values, tokens, and request parameters. <br>
Mitigation: Mask sensitive log fields in final and intermediate output, including IP addresses, cookies, authorization values, tokens, and query parameter values. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Common DDoS Pro Block Reasons and Recommendations](references/common-block-reasons.md) <br>
- [Domain Security Policy Management](references/domain-security-policy.md) <br>
- [RAM Policy Requirements](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [DDoS Pro Rule Configuration Details](references/rule-config-details.md) <br>
- [DDoS Pro Rule Operation Policy](references/rule-operations.md) <br>
- [Success Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks sensitive log values and requires user confirmation for customizable parameters.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

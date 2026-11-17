## Description:

Diagnoses why a request was blocked by Alibaba Cloud WAF by retrieving block logs, identifying the triggering rule, and providing remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to investigate Alibaba Cloud WAF interception events from a request ID, retrieve WAF/SLS evidence, identify triggering rules, and produce remediation guidance. When granted explicit permissions, it can also guide WAF log collection changes and rule status disable operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use Alibaba Cloud credentials to query WAF and SLS resources, which can expose operational log data to the agent.

Mitigation: Start with read-only RAM permissions and scope SLS access to the needed WAF projects and logstores.

Risk: If modification permissions are granted, the skill can change WAF logging settings or disable WAF rules.

Mitigation: Grant modification permissions only for approved sessions, require explicit user confirmation before writes, and follow check-then-act behavior before changing state.

Risk: The skill asks for persistent Aliyun CLI auto-plugin installation and plugin updates.

Mitigation: Review CLI plugin changes separately and avoid global plugin updates in managed environments unless they are approved.

## Reference(s):

- [RAM Policy Requirements](references/ram-policies.md)
- [Common WAF Block Reasons and Recommendations](references/common-block-reasons.md)
- [WAF Rule Configuration Details](references/rule-config-details.md)
- [WAF Rule Operation Policy](references/rule-operations.md)
- [Aliyun CLI installation documentation](https://help.aliyun.com/document_detail/139508.html)
- [Alibaba Cloud WAF OpenAPI documentation](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and structured analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked WAF/SLS log details, rule identifiers, remediation recommendations, and optional configuration or rule-status change guidance.]

## Skill Version(s):

0.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

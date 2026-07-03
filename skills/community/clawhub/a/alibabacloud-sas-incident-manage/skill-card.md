## Description: <br>
Alibaba Cloud Security Center incident management skill for querying security incidents, threat trends, and incident details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operations engineers and cloud administrators use this skill to query Alibaba Cloud Security Center incidents, inspect incident details, and summarize threat trends through the Aliyun Cloud SIEM CLI plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers can lead to live security-data queries using the user's configured Alibaba Cloud credentials. <br>
Mitigation: Review before installation, use only authorized Alibaba Cloud accounts, and require explicit confirmation before live incident queries. <br>
Risk: Live cloud queries may expose security incident details or infrastructure identifiers in user-facing output. <br>
Mitigation: Summarize incident data, mask raw IP addresses and unnecessary instance IDs, and avoid dumping raw API responses. <br>
Risk: Overprivileged or long-lived credentials increase impact if the configured cloud profile is misused. <br>
Mitigation: Use a least-privilege RAM user or temporary credentials with only the incident query permissions required by the skill. <br>
Risk: Incorrect product, API version, or region selection can produce failed or misleading incident-query results. <br>
Mitigation: Use the cloud-siem CLI plugin, required API versions, explicit region flags, and the documented timeout and error-handling behavior. <br>


## Reference(s): <br>
- [RAM permission policy](references/ram-policies.md) <br>
- [Command syntax and parameters](references/related-commands.md) <br>
- [Correct usage patterns](references/acceptance-criteria.md) <br>
- [Verification methods](references/verification-method.md) <br>
- [CLI installation guide](references/cli-installation-guide.md) <br>
- [Cloud SIEM API Documentation](https://api.aliyun.com/product/cloud-siem) <br>
- [ListIncidents API](https://api.aliyun.com/api/cloud-siem/2024-12-12/ListIncidents?useCommon=true) <br>
- [GetIncident API](https://api.aliyun.com/api/cloud-siem/2024-12-12/GetIncident?useCommon=true) <br>
- [DescribeEventCountByThreatLevel API](https://api.aliyun.com/api/cloud-siem/2022-06-16/DescribeEventCountByThreatLevel?useCommon=true) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized incident findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks sensitive incident details in user-facing output and requires per-session user-agent tracing.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

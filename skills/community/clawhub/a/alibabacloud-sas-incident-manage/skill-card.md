## Description: <br>
Alibaba Cloud Security Center incident management skill for querying security incidents, threat trends, and incident details through Aliyun CLI and the cloud-siem plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and cloud operators use this skill to inspect Alibaba Cloud Security Center incidents, retrieve incident details, and summarize threat trends from configured Aliyun CLI credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's Alibaba Cloud credentials to read sensitive Security Center incident data. <br>
Mitigation: Use a least-privilege RAM user or temporary role, protect Aliyun CLI configuration files, and avoid exposing AccessKey secrets in commands or chat. <br>
Risk: Incident results can reveal infrastructure identifiers, IP addresses, and security posture details. <br>
Mitigation: Summarize findings for end users, mask sensitive values where possible, and review outputs before sharing them outside the authorized response team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-sas-incident-manage) <br>
- [Related Commands - Cloud SIEM Incident Management](references/related-commands.md) <br>
- [RAM Policies - Cloud Security Center Incident Management](references/ram-policies.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Verification Methods - Cloud Security Center Incident Management](references/verification-method.md) <br>
- [Acceptance Criteria - alibabacloud-sas-incident-manage](references/acceptance-criteria.md) <br>
- [Cloud SIEM API Documentation](https://api.aliyun.com/product/cloud-siem) <br>
- [RAM Policy Syntax](https://help.aliyun.com/document_detail/28664.html) <br>
- [Cloud Security Center API Permissions](https://help.aliyun.com/document_detail/28674.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline Aliyun CLI commands and summarized incident findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks sensitive incident details in user-facing summaries and relies on preconfigured Aliyun CLI credentials.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

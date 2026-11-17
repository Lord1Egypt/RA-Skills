## Description:

Alibaba Cloud Security Center incident management skill for querying security incidents, threat trends, and incident details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Security operations teams, cloud administrators, and agents use this skill to query Alibaba Cloud Cloud SIEM incidents, retrieve incident details, and summarize threat trends through the Aliyun CLI.

### Deployment Geography for Use:

China (Shanghai) and Singapore service regions

## Known Risks and Mitigations:

Risk: Credential exposure through command lines, chat, CI logs, scripts, or setup examples.

Mitigation: Use a least-privilege RAM identity and prefer interactive configuration, workload identity, or a secret manager instead of passing access keys or STS tokens through visible channels.

Risk: Unverified Aliyun CLI, plugin, or Python dependency installation can introduce supply-chain risk.

Mitigation: Pin and verify the Aliyun CLI, cloud-siem plugin, and Python dependencies before installing or using the skill.

Risk: Detailed incident retrieval may expose sensitive security event information.

Mitigation: Confirm before retrieving detailed incident records, summarize results, and redact sensitive IP addresses and resource identifiers in user-facing output.

## Reference(s):

- [Main skill documentation](artifact/SKILL.md)
- [Related commands](artifact/references/related-commands.md)
- [RAM policies](artifact/references/ram-policies.md)
- [Verification methods](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [Cloud SIEM API documentation](https://api.aliyun.com/product/cloud-siem)
- [ListIncidents API](https://api.aliyun.com/api/cloud-siem/2024-12-12/ListIncidents?useCommon=true)
- [GetIncident API](https://api.aliyun.com/api/cloud-siem/2024-12-12/GetIncident?useCommon=true)
- [DescribeEventCountByThreatLevel API](https://api.aliyun.com/api/cloud-siem/2022-06-16/DescribeEventCountByThreatLevel?useCommon=true)
- [RAM policy syntax](https://help.aliyun.com/document_detail/28664.html)
- [Cloud Security Center API permissions](https://help.aliyun.com/document_detail/28674.html)
- [Official Aliyun CLI documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes incident data, redacts sensitive IP and resource details, and avoids dumping raw API responses in user-facing output.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Alibaba Cloud Security Center (SAS) CWPP host security alert handling skill for querying, analyzing, and handling Cloud Security Center alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Security operators and cloud engineers use this skill to review Alibaba Cloud Security Center CWPP alerts, inspect available handling operations, choose remediation actions, and verify handling status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide production-impacting remediation such as blocking IPs, quarantining files, killing processes, ignoring alerts, whitelisting future matches, or disabling defenses.

Mitigation: Require explicit operator approval before remediation, query available operations per alert, execute only operations where UserCanOperate is true, and prefer read-only or least-privilege RAM permissions until handling is approved.

Risk: Setup guidance includes curl-to-bash, latest binary downloads, and plugin update paths that can introduce unverified dependencies.

Mitigation: Install Aliyun CLI from independently verified sources, pin or verify CLI and plugin versions, and avoid automatic installer paths in sensitive environments.

Risk: The workflow requires Alibaba Cloud credentials and may expose high-impact cloud access if long-lived or privileged credentials are used.

Mitigation: Use temporary credentials or RAM roles where possible, avoid root or administrator credentials, do not paste long-lived access keys into shell commands, and follow least-privilege RAM policies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-sas-alert-handler)
- [Workflow Details](artifact/references/workflow-details.md)
- [Related APIs](artifact/references/related-apis.md)
- [Operation Codes Reference](artifact/references/operation-codes.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [Error Handling Guide](artifact/references/error-handling.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Aliyun CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Aliyun CLI Official Documentation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI Repository](https://github.com/aliyun/aliyun-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommendations, CLI command patterns, remediation status summaries, and operator-facing error guidance.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

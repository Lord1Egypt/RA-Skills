## Description:

Guides agents through Alibaba Cloud Security Center vulnerability queries, repair workflows, post-fix verification, error-code troubleshooting, and manual remediation paths for non-standard systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security operators, DevOps engineers, and agents assisting them use this skill to inspect Alibaba Cloud SAS vulnerability records, plan repairs, execute confirmed remediation actions, and verify closure. It is especially useful when repair status, quota, endpoint, credential, reboot, or non-standard host conditions need structured handling.

### Deployment Geography for Use:

Global, subject to Alibaba Cloud Security Center account site and endpoint availability.

## Known Risks and Mitigations:

Risk: Installation and credential setup may expose AccessKey secrets or execute installer commands without enough review.

Mitigation: Review the CLI installation and credential sections first, prefer verified package-manager installation paths, and avoid pasting or storing AccessKey secrets through agent-driven commands.

Risk: Repair workflows can run privileged or API-returned commands on affected servers.

Mitigation: Validate the exact command and affected assets before execution, use least-privilege SAS permissions, and require backups or snapshots before privileged repairs.

Risk: Some repair and verification operations can affect production availability through reboots, scan scope changes, billing, or full-account scans.

Mitigation: Present the change list, reboot impact, billing note, and scope before write operations, then execute only after explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-sas-vul-repair)
- [Alibaba Cloud Security Center vulnerability management](https://help.aliyun.com/zh/security-center/user-guide/vulnerability-management/)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [SAS API reference](references/api-reference.md)
- [RAM policies](references/ram-policies.md)
- [Vulnerability query scenario](references/scenario-query.md)
- [Vulnerability repair scenario](references/scenario-repair.md)
- [Repair error scenarios](references/scenario-errors.md)
- [Recheck and verification scenario](references/scenario-recheck.md)
- [Non-standard system scenario](references/scenario-nonstandard.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Related commands](references/related-commands.md)
- [Documentation lookup strategy](references/doc-lookup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, command tables, decision guidance, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmed Alibaba Cloud CLI commands and JSON command parameters for SAS operations.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manage multiple Alibaba Cloud accounts and batch-export Security Center (SAS) baseline and vulnerability reports via the aliyun CLI and Python scripts. Supports account list refresh, enable/disable, concurrent batch export of cloud platform configuration check (baselineCspm), system baseline risk (exportHcWarning), attack path event (exportAttackPathEvent), Linux/Windows/application/emergency vulnerability results across all managed accounts. Use this skill when users need to manage SAS multi-account settings, export baseline or vulnerability compliance data, or merge multi-account security reports into a single file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud account administrators and security engineers use this skill to manage resource-directory accounts and consolidate Security Center baseline, attack-path, and vulnerability findings across selected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported reports may contain sensitive account and security findings.

Mitigation: Use narrowly authorized Alibaba Cloud credentials and store reports in a dedicated private directory.

Risk: Batch exports include every account currently enabled in the local account list.

Mitigation: Review enabled accounts and the requested export scope before running an export.

Risk: Setup changes CLI plugins and persists AI-mode settings, and reruns can replace same-day output files.

Mitigation: Review setup commands before applying them and preserve any same-day reports that must be retained.

## Reference(s):

- [Skill release page](https://clawhub.ai/sdk-team/skills/alibabacloud-sas-multiaccount-manage)
- [RAM Policy Reference](references/ram-policies.md)
- [Alibaba Cloud CLI releases](https://github.com/aliyun/aliyun-cli/releases)
- [Security Center RAM authorization](https://www.alibabacloud.com/help/en/security-center/developer-reference/api-sas-2018-12-03-ram)
- [STS GetCallerIdentity](https://www.alibabacloud.com/help/en/resource-access-management/latest/getcalleridentity)

## Skill Output:

**Output Type(s):** [Files, Configuration]

**Output Format:** [Excel (.xlsx) security reports and JSON account configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Merged reports include account identifiers and display names and use date-stamped filenames.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

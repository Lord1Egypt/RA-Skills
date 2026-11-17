## Description:

Provides read-only health reports and bounded fleet scans for Alibaba Cloud SASE (CSAS) endpoint devices, covering CPU, memory, battery, disk, and reporting status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and endpoint administrators use this skill to investigate a device's performance and reporting status or identify recent health risks across a bounded CSAS fleet without modifying devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI through a remote shell script or automatically installing its CSAS plugin runs third-party code locally.

Mitigation: Review the CLI installation source before running it, and approve local plugin installation.

Risk: An unintended profile, region, device scope, scan limit, or resume-file path can expose or retain device data outside the intended scope.

Mitigation: Confirm a read-only profile and the exact cloud and local scan scope before making calls.

Risk: Missing or stale device telemetry can make health conclusions misleading.

Mitigation: Report incomplete telemetry as insufficient data and distinguish reporting recency from device status.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-csas-device-health-monitor)
- [CSAS API contract](references/api-contract.md)
- [Required RAM permissions](references/ram-policies.md)
- [Operational limits](references/operational-limits.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Local scan resume file](references/state-files.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown guidance and JSON device or fleet reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each command returns one JSON result; an optional local file tracks scan progress.]

## Skill Version(s):

0.0.1 (source: ClawHub release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

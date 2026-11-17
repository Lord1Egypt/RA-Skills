## Description:

Diagnoses Alibaba Cloud Live stream quality, CDN connectivity, and traffic abuse; records or snapshots user-provided streams and generates signed push/pull test URLs without changing cloud configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to investigate Alibaba Cloud Live playback, ingest, CDN, and traffic-theft issues, obtain read-only diagnostics, capture local stream samples, and generate test URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud diagnostics can expose live-domain configuration and access-log data.

Mitigation: Grant only the read-only Alibaba Cloud Live permissions required for the investigation and review access before running cloud queries.

Risk: Recording or snapshot commands create local media files.

Mitigation: Confirm the target, destination, and duration before capture; use a dry run if unsure.

Risk: Verbose node geolocation sends CDN node IP addresses to ipinfo.io.

Mitigation: Avoid verbose node geolocation unless sharing those IP addresses is acceptable.

Risk: Recorder stop commands may affect unrelated recordings.

Mitigation: Use stop commands only for recordings created by this tool.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-live-assistant)
- [Alibaba Cloud Live security overview](https://help.aliyun.com/zh/live/user-guide/security-overview/)
- [Read-only RAM policy](artifact/references/ram-policies.md)
- [Stream quality troubleshooting](artifact/references/stream-quality-troubleshooting.md)
- [Security hardening guide](artifact/references/security-hardening-guide.md)

## Skill Output:

**Output Type(s):** [JSON diagnostics, Markdown guidance, Shell commands, Signed stream URLs, Local recordings and snapshots]

**Output Format:** [JSON from diagnostic scripts; human-readable analysis and guidance; optional local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided stream URL or domain; recordings and snapshots are written locally to a confirmed output path.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

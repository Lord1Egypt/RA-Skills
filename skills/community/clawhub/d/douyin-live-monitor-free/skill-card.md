## Description:

Monitors public Douyin live rooms for a bounded period, recording timestamped status snapshots and reporting changes while the task runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, community managers, and other users can check one or more public Douyin live rooms over a user-defined period, capture status and title changes, and save a concise report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial: one referenced script was only partially inspected and one reference remained unresolved.

Mitigation: Review the external download and source instructions and confirm that you trust those sources before installation.

Risk: The skill operates through an existing browser session, which may contain account-specific pages or data.

Mitigation: Use only the precisely selected browser, read public page fields only, and stop at login, verification, or security challenges.

## Reference(s):

- [EasyBR official download page](https://www.ebrower.com/down.html)
- [EasyBR GitHub release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)
- [Easy WebBridge source](https://github.com/aiispower/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Markdown]

**Output Format:** [Timestamped live-room snapshots and status-change reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional JSON, CSV, or Markdown files; monitoring and status updates end with the active task.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

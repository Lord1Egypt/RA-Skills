## Description:

Generates scheduled Douyin hot-list reports by fetching trending videos, using an OpenClaw model to produce structured analysis notes, writing Markdown and Word outputs, and emailing the report to configured recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[link-1069](https://clawhub.ai/user/link-1069)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate recurring Douyin trend monitoring, generate concise analysis reports, and distribute them by email. It is suited to configured environments with explicit recipient, SMTP, TikHub, and OpenClaw access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation can send reports without an explicit per-run decision.

Mitigation: Make cron setup opt-in and require review of the schedule before enabling recurring execution.

Risk: Hardcoded or default external recipients can send generated reports to unintended addresses.

Mitigation: Remove bundled recipient defaults and require explicit recipient confirmation before any email send.

Risk: SMTP and TikHub credentials are needed for normal operation.

Mitigation: Store credentials only in user-controlled environment or configuration files and apply least-privilege access.

Risk: An exposed web UI or misleading browser key-handling behavior could disclose credentials.

Mitigation: Bind web services to localhost with authentication and avoid entering API keys into the browser UI until key handling is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/link-1069/skills/douyin-analyse-batch)
- [Deployment guide](artifact/references/DEPLOY.md)
- [TikHub registration](https://user.tikhub.io)
- [SiliconFlow API](https://cloud.siliconflow.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report, DOCX attachment, shell commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create scheduled cron execution, local report files, and outbound email when configured.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Tracks configured Beijing Housing Commission new-home projects, crawls signed-room and project summary data, estimates newly signed average prices, writes rows to a Feishu spreadsheet, and sends Feishu direct-message notifications after each run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronstuart](https://clawhub.ai/user/aaronstuart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor Beijing pre-sale housing projects, maintain project mappings, sync newly signed rooms into a Feishu ledger, estimate average prices for new signings, and notify stakeholders of updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the artifact ships a real Feishu credential.

Mitigation: Revoke the bundled secret, remove it from configuration, and supply Feishu credentials only through protected environment variables or secret storage before installation.

Risk: The release evidence reports an under-documented cron-run monitor that can send local OpenClaw run-log details to Feishu.

Mitigation: Remove the monitor or make it explicit opt-in with a user-controlled run-log path, recipient, and redacted notification payloads.

Risk: The release evidence advises restricting project URL fetching to the intended Beijing Housing Commission host.

Mitigation: Validate configured project URLs against bjjs.zjw.beijing.gov.cn before running sync jobs.

Risk: The release evidence notes that housing data, cache-derived room details, and run notifications are sent to Feishu.

Mitigation: Confirm that Feishu is an approved destination for this data and limit spreadsheet and message access to intended recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronstuart/skills/beijing-signed-price-tracker)
- [Beijing Housing Commission project portal](http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320794&projectID=8138177&systemID=2&srcId=1)
- [Feishu Open Platform API base](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON cache and sync report files when the provided scripts run.]

## Skill Version(s):

1.6.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

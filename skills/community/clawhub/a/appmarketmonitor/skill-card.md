## Description:

华为应用市场 AppGallery 批量查询应用版本、更新说明和用户评论，并输出 PDF 汇总报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasoncod](https://clawhub.ai/user/jasoncod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operations teams use this skill to monitor batches of apps in Huawei AppGallery, collect version/update details and recent user-review signals, and receive a tabular PDF report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attached spreadsheets may contain unrelated sensitive columns even though the workflow only needs app names and optional update dates.

Mitigation: Attach a minimal spreadsheet containing only the app-name column and, when needed, the Android update-date column.

Risk: Public app-store lookups through a phone GUI can miss fields or return incomplete results.

Mitigation: Use the documented serial lookup, retry, and data-gap recording flow before relying on the final report.

## Reference(s):

- [Huawei AppGallery](https://appgallery.cloud.huawei.com)
- [ClawHub skill release](https://clawhub.ai/jasoncod/skills/appmarketmonitor)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [PDF report with tabular app update, version-history, rating, and recent negative-review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided app names and optional Android update dates from an attached spreadsheet; records unresolved data gaps when lookup retries still fail.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

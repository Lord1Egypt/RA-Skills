## Description:

Exports Douyin user profile video data through the TikHub API and can optionally export DOU+/BOSS promotion order data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, operators, and developers use this skill to export a Douyin account's video list and optional paid promotion order data into local JSON, CSV, or Excel files for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive API tokens and business export data.

Mitigation: Use only authorized tokens, avoid passing bearer tokens on the command line, and store exports in a protected location.

Risk: Generated CSV files may include remote text fields that are unsafe to open directly in spreadsheet software.

Mitigation: Sanitize exported text fields before opening CSV files in a spreadsheet.

Risk: The DOU+/BOSS export is a separate sensitive business-data capability.

Mitigation: Review and approve that capability separately from the Douyin video export workflow before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ahsbnb/skills/douyin-data-exporter)
- [TikHub Registration](https://user.tikhub.io/register)
- [TikHub API Base](https://api.tikhub.io/api/v1)

## Skill Output:

**Output Type(s):** [Files, JSON, CSV, Excel, Shell commands]

**Output Format:** [Local JSON, CSV, Excel, and summary report files, with a REPORT_PATH line on stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and authorized API tokens; export files may contain sensitive account, video, promotion, or business data.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Daily Viz helps users record mood, exercise, sleep, and work hours, then view charts, reports, and habit insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaooojun](https://clawhub.ai/user/xiaooojun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to track daily wellness and productivity signals, summarize recent activity, and generate simple visual reports for habit building and self-improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal wellness and productivity records in a local JSON file under the user's home directory. <br>
Mitigation: Use it only for information the user is comfortable storing locally, and manage local file access, backup, and deletion according to the user's privacy needs. <br>
Risk: Export, share, cloud-sync, and encryption claims are under-specified in the available evidence. <br>
Mitigation: Do not rely on those claims for sensitive data unless a future version clearly documents what leaves the device, where it is stored, and how deletion and encryption work. <br>


## Reference(s): <br>
- [Daily Viz ClawHub listing](https://clawhub.ai/xiaooojun/daily-viz) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown and text guidance with local JSON records and console chart or report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-entered records locally under ~/.daily-viz/data/records.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, _meta.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

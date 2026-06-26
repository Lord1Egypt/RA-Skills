## Description: <br>
Monitor disk space across drives, alert before disks fill up, track usage trends, find large directories, and suggest cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and system operators use this skill to monitor local disk usage, detect warning or critical storage levels, review usage trends, and identify large directories for cleanup planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local disk-usage commands and scans directory names and sizes when asked. <br>
Mitigation: Review the directories before scanning and avoid sensitive paths when file names or storage patterns should not appear in output or logs. <br>
Risk: The skill stores recent disk usage history locally in a temporary file. <br>
Mitigation: Use the default local-only behavior only on trusted systems, or configure the history file location according to local retention and access-control expectations. <br>


## Reference(s): <br>
- [Disk Watch ClawHub page](https://clawhub.ai/TheShadowRose/disk-watch) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with JavaScript examples and disk status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local paths, drive usage percentages, large directory listings, cleanup suggestions, and recent usage trends.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

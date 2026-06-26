## Description: <br>
Query China Railway 12306 for train schedules, remaining tickets, and station information for train, high-speed rail, and ticket availability requests within China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danihe001](https://clawhub.ai/user/danihe001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check China Railway train schedules, remaining ticket availability, seat classes, and station matches for domestic rail travel in China. It supports filtered searches by train type, departure or arrival time, duration, seat type, and bookable status. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to China Railway 12306 services. <br>
Mitigation: Use it only when 12306 train schedule or ticket availability lookups are expected and network access to 12306 is acceptable. <br>
Risk: HTML mode can write result files to a default or user-specified local output path. <br>
Mitigation: Review any custom output path before running the skill to avoid overwriting files that should be preserved. <br>


## Reference(s): <br>
- [ClawHub 12306 Backup release](https://clawhub.ai/danihe001/12306-backup) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [China Railway 12306](https://www.12306.cn/index/) <br>
- [12306 ticket query page](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown tables, JSON, text paths, or saved HTML files from Node.js command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local HTML result files and cache station data locally for 7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

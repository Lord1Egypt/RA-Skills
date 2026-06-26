## Description: <br>
Query China Railway 12306 for train schedules, remaining tickets, and station info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangsaizz](https://clawhub.ai/user/zhangsaizz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, assistants, and operators use this skill to check China Railway 12306 schedules, remaining ticket availability, and station information for travel within China. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route, station, and travel-date queries are sent to China Railway 12306. <br>
Mitigation: Use the skill for ordinary schedule and remaining-ticket lookups, and avoid submitting sensitive travel searches through it. <br>
Risk: HTML output can create or overwrite the selected local output path. <br>
Mitigation: Choose an output path that is safe to create or replace before running HTML mode. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangsaizz/12306-query) <br>
- [China Railway 12306 left-ticket query entry](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc) <br>
- [China Railway 12306 station data index](https://www.12306.cn/index/) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown table, JSON, or an HTML file path depending on selected options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The default HTML mode writes a local file and prints its path; Markdown and JSON modes print to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

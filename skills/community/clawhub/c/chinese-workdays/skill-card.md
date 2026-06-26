## Description: <br>
Calculate legal working days in China according to official government holiday schedules, excluding weekends and public holidays while including makeup workdays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manucode2000-max](https://clawhub.ai/user/manucode2000-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to calculate legal workday counts for China mainland date ranges, months, quarters, and full years. It is most useful for planning, scheduling, and lightweight calendar analysis where Chinese public holidays and makeup workdays matter. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Unsupported or generated holiday schedules may be presented as official. <br>
Mitigation: Verify each YAML calendar against State Council notices and avoid relying on years without confirmed source data. <br>
Risk: Incorrect workday counts could affect payroll, compliance, contracts, attendance, or operational planning. <br>
Mitigation: Use reviewed calendar data and human approval before applying results to high-impact business decisions. <br>


## Reference(s): <br>
- [Chinese Workdays ClawHub listing](https://clawhub.ai/manucode2000-max/chinese-workdays) <br>
- [State Council Gazette holiday notices](https://www.gov.cn/gongbao/) <br>
- [2007 State Council holiday notice](https://www.gov.cn/zhengce/content/2008-03/28/content_1761.htm) <br>
- [2008 State Council holiday notice](https://www.gov.cn/zhengce/content/2008-03/28/content_1645.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; CLI output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workday counts and optional holiday listings for date ranges, months, quarters, or years.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence; artifact documentation mentions 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

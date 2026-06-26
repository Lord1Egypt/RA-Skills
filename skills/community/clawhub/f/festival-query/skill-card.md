## Description: <br>
节日查询工具，支持中国农历日期、传统节日、二十四节气、欧美主流节日查询，并支持按日期、年份、月份或节气表查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhou-xiaobo](https://clawhub.ai/user/zhou-xiaobo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent workflows use this skill to answer holiday, lunar calendar, solar term, and Western festival questions for a specific date, year, or month. It is useful when a task needs concise calendar lookup results rather than broad web research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented dependency install command uses --break-system-packages and can modify system Python environments. <br>
Mitigation: Install zhdate and holidays in a Python virtual environment, and pin dependency versions when reproducible or tightly controlled installs are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhou-xiaobo/festival-query) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhou-xiaobo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text returned by a Python CLI, with Markdown shell command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include calendar dates, lunar date information, festival names, solar terms, and user-facing error messages for invalid date formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

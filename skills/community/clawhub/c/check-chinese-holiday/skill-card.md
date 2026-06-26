## Description: <br>
基于 chinesecalendar 包的中国节假日检测，判断是否为节假日/调休日工作日。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuehongyanL](https://clawhub.ai/user/xuehongyanL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check whether a China calendar date is a legal holiday, adjusted workday, ordinary weekend, or reminder-worthy workday. It also reports whether the local chinesecalendar dependency appears current enough for the current year. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the local chinesecalendar Python package, whose holiday data can become outdated. <br>
Mitigation: Use a virtual environment, review any suggested pip install or upgrade command before running it, and confirm the package supports the queried year. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuehongyanL/check-chinese-holiday) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs date status, workday or holiday classification, reminder guidance, and local package freshness status.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

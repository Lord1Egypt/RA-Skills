## Description: <br>
Calculates Bazi chart, major luck cycle, and annual fortune information from gender and an ISO 8601 birth timestamp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahaofan](https://clawhub.ai/user/ahaofan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a Python command-line tool that submits gender and birth timestamp inputs to the Bagezi Bazi API and returns chart data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends gender, birth timestamp, and any supplied name to api.bagezi.top over unencrypted HTTP. <br>
Mitigation: Use only if this data sharing is acceptable; omit or replace the name when possible and avoid entering birth details considered sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahaofan/bazi) <br>
- [凡心八字官网](http://bagezi.top/) <br>
- [Bagezi Paipan API endpoint](http://api.bagezi.top/api/paipan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gender and birthday_str; name is optional and defaults to 张三.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

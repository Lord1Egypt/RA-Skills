## Description: <br>
查询永东直通巴士（eebus）班次、票价和余座，支持中文自然语言输入并解析日期、上车点和下车点。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porridgec](https://clawhub.ai/user/porridgec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Yongdong/eebus cross-border bus schedules, fares, and remaining seats for Hong Kong and Shenzhen routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries contact www.myeebus.com and disclose the requested route, date, stops, and the user's IP address to that service. <br>
Mitigation: Use the skill only when an eebus lookup is intended, and avoid submitting sensitive or unnecessary travel details. <br>
Risk: Broad trigger wording may activate the skill for general Hong Kong or Shenzhen travel questions. <br>
Mitigation: Confirm that the user wants an eebus bus lookup before running the query script. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary of queried route, date, fares, departure and arrival times, and remaining seats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Node.js script that queries www.myeebus.com for bus availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

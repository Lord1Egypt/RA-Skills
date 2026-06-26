## Description: <br>
Fetches driving-license practice questions for car, bus, truck, and motorcycle exams covering subject one and subject four. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve JisuAPI driving-exam question-bank entries and build conversational practice flows for Chinese driving-license subject one and subject four exams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests send the JISU_API_KEY and exam parameters to JisuAPI, which may affect credential exposure, provider quota, or billing. <br>
Mitigation: Use a dedicated JISU_API_KEY where possible, restrict and rotate it according to provider controls, and monitor JisuAPI quota and billing. <br>
Risk: The skill depends on JisuAPI availability and the provider's driving-exam data quality. <br>
Mitigation: Handle API errors and stale or unexpected responses in the calling agent, and verify exam guidance against authoritative materials when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/driverexam) <br>
- [JisuAPI Driver Exam API documentation](https://www.jisuapi.com/api/driverexam/) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands; runtime output is JSON from the JisuAPI result field.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends license type, subject, pagination, sort, and optional chapter parameters to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

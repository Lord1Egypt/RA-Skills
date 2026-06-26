## Description: <br>
职业发展助手为职业院校学生、教师和职场新人提供职业介绍、技能证书、职教政策、就业指导和职业规划支持。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, teachers, career changers, and early-career professionals use this skill to explore career paths, compare certificates, understand vocational education policies, prepare resumes and interviews, and generate career recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional commercial API mode may send profile, resume, career-interest, or employment data to a configured endpoint. <br>
Mitigation: Use offline mode by default; enable API mode only with a trusted endpoint and review what data may be sent before entering CAREER_API_KEY. <br>
Risk: Career, salary, certificate, and vocational-policy guidance may become outdated or vary by region. <br>
Mitigation: Present recommendations as reference material and direct users to official channels before they make education, certification, employment, or financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/career-development-assistant) <br>
- [热门职业数据库](references/careers.md) <br>
- [技能证书指南参考](references/certificates.md) <br>
- [职教政策知识库](references/vocational-policy.md) <br>
- [就业指导参考](references/employment-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON or terminal output from the career recommendation script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default offline mode uses the bundled knowledge base; optional API mode requires a trusted endpoint and CAREER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

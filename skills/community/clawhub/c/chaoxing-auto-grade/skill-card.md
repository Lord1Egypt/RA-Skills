## Description: <br>
Automates Chaoxing Learning Pass assignment grading by using Playwright to find ungraded subjective responses, call Tongyi Qianwen for scores, and submit grades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenghaozhangswu](https://clawhub.ai/user/chenghaozhangswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers or course operators can use this skill to automate grading workflows for Chaoxing subjective assignments, including login, course selection, ungraded assignment discovery, AI scoring, and score submission. It should only be used by authorized staff who may process student submissions and grades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically submit grades to Chaoxing. <br>
Mitigation: Use it only with explicit authorization, test first on non-production data, and manually review proposed scores before applying them to real student records. <br>
Risk: Student answers may be sent to Tongyi Qianwen/DashScope for scoring. <br>
Mitigation: Confirm that the course operator is permitted to share the relevant student submissions with that third-party AI service before use. <br>
Risk: Chaoxing credentials and a DashScope API key are stored in config.json. <br>
Mitigation: Keep config.json private, avoid committing it, and use a dedicated least-privilege account when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenghaozhangswu/chaoxing-auto-grade) <br>
- [Playwright](https://playwright.dev/) <br>
- [DashScope Tongyi Qianwen documentation](https://help.aliyun.com/zh/dashscope/) <br>
- [Aliyun Bailian console](https://bailian.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local config.json for Chaoxing credentials, DashScope API key, model, score range, course name, and optional Chrome path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

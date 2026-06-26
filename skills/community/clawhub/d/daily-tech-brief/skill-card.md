## Description: <br>
生成每日科技摘要，行业新闻为主体，OpenClaw 为固定板块，ClawHub 信息优先使用命令行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gift-is-coding](https://clawhub.ai/user/gift-is-coding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and content teams use this skill to create a Chinese daily technology briefing or podcast outline focused on industry news, Elon Musk, Tesla, xAI, AI companies, OpenClaw updates, and ClawHub skill activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cron workflow can run a caller-specified podcast or briefing script without clear limits. <br>
Mitigation: Use the cron workflow only with a trusted fixed script path, review what that script can read, write, publish, or upload, and do not let untrusted prompts or callers choose arbitrary commands. <br>


## Reference(s): <br>
- [Daily Tech Brief on ClawHub](https://clawhub.ai/gift-is-coding/daily-tech-brief) <br>
- [gift-is-coding publisher profile](https://clawhub.ai/user/gift-is-coding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing in Chinese with cited source links and optional execution status details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes source-verified industry news, includes fixed OpenClaw and ClawHub sections, and reports any ClawHub CLI fallback reason.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

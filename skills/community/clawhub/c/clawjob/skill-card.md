## Description: <br>
UP 简历 AI 求职助手，用于创建和编辑简历、搜索校招/社招/实习岗位、按 JD 优化简历、生成每日职位简报并指导投递。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HelloSanshi](https://clawhub.ai/user/HelloSanshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers, students, and career switchers use this skill to manage resumes, search internships and jobs, optimize resume content against job descriptions, set up job monitoring, and prepare application form content through the UP 简历 MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive resume, contact, education, employment, and application data. <br>
Mitigation: Review generated resume content and application field mappings before submission, keep the API key secret, and avoid storing ID numbers or other high-sensitivity application values in ATS records. <br>
Risk: Resume update and delete workflows can change or remove user resume data through MCP tools. <br>
Mitigation: Approve substantive edits and delete actions only after reviewing the proposed changes, especially for full resume deletion or section deletion. <br>
Risk: The job-monitor workflow can create recurring local cron or launchd tasks. <br>
Mitigation: Enable daily monitoring only when a persistent local task is intended, and keep the stop or unload commands with the generated monitor configuration. <br>
Risk: The skill depends on the third-party @upcv/mcp-server package and UP 简历 service. <br>
Mitigation: Install and use the MCP server only if the user trusts UP 简历 and the package source. <br>


## Reference(s): <br>
- [UP 简历 website](https://upcv.tech) <br>
- [Clawjob OpenClaw release page](https://clawjob.upcv.tech) <br>
- [ClawHub skill page](https://clawhub.ai/HelloSanshi/clawjob) <br>
- [UPCV MCP Server](https://github.com/HireTechUpUp/upcv-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands, structured resume/job-search summaries, monitor setup snippets, and ATS field mappings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MCP tool usage, resume edits, PDF export links, local monitor scripts, cron or launchd configuration, and reusable ATS records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

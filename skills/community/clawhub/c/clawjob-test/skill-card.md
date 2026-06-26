## Description: <br>
UP 简历 AI 求职助手 helps users create and optimize resumes, search campus, internship, and social-hire jobs, monitor new opportunities, and prepare application materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HelloSanshi](https://clawhub.ai/user/HelloSanshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers and students use this skill to manage resumes, search job and campus recruiting data, compare resumes against job descriptions, receive daily opportunity briefings, and prepare application form content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive resume, job-search, and application data and requires API-key access to the UPCV MCP server. <br>
Mitigation: Install only if the publisher and UPCV MCP server are trusted, and avoid storing ID numbers, photos, secrets, or filled application values in ATS records. <br>
Risk: The job monitoring workflow can create persistent local automation through scripts and scheduled tasks. <br>
Mitigation: Review generated scripts, scheduled tasks, target files, and commands before enabling monitoring, and remove only this skill's cron or launchd entry when disabling it. <br>
Risk: Resume optimization and application guidance could introduce inaccurate or unsupported claims if accepted without review. <br>
Mitigation: Review proposed resume edits before saving or submitting them, and keep changes grounded in the user's actual experience and the target job description. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HelloSanshi/clawjob-test) <br>
- [UP 简历](https://upcv.tech) <br>
- [Clawjob OpenClaw edition](https://clawjob.upcv.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, structured text, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate resume and application guidance, monitoring setup commands, daily report content, and ATS notes when the user approves those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

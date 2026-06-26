## Description: <br>
Daily work report skill that logs work through conversation, writes records to Tencent Docs, and generates monthly summaries with one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmww](https://clawhub.ai/user/nmww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees in a teaching and research team use this skill to record daily work, leave, and overtime entries in Tencent Docs, then prepare monthly summaries from those records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monthly read and summary features can read and summarize coworkers' records from a shared Tencent Docs sheet. <br>
Mitigation: Use only with an intentionally connected Tencent Docs workspace, require user-level filtering before relying on monthly features, and restrict Tencent Docs sharing to approved users. <br>
Risk: The skill requires Tencent Docs OAuth credentials and writes work-report data to an online spreadsheet. <br>
Mitigation: Limit spreadsheet permissions, avoid broad editable access for attendance or project details, and revoke or rotate authorization if credentials are exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nmww/daily-report-assistant) <br>
- [Data schema](references/data-schema.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Deployment guide](references/deploy-guide.md) <br>
- [Tencent Docs authorization](https://docs.qq.com/scenario/open-claw.html?nlc=1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented status text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, mcporter, and Tencent Docs OAuth credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

UP 简历 AI 求职助手 helps users create and edit professional resumes, search campus, social, and internship roles, compare resumes against job descriptions, monitor new openings, and prepare application materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellosanshi](https://clawhub.ai/user/hellosanshi)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers, students, and career switchers use this skill to manage the job search workflow in an agent: resume creation and editing, role discovery, job-description alignment, daily job monitoring, and application preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daily monitoring workflow can create persistent scheduled agent execution through a local monitor script and launchd or cron task.

Mitigation: Prefer one-time searches unless scheduled monitoring is intentional, and inspect the generated script and scheduled task before enabling them.

Risk: The MCP setup flow uses an API key and may expose secrets if they are passed directly on the command line or retained in shell history.

Mitigation: Use local secret-handling practices that avoid exposing API keys in shared terminals, logs, or command history.

Risk: The setup command installs an MCP package through npx, which can change over time if the package version is not pinned.

Mitigation: Review the package before installation and pin the MCP server version when reproducibility or supply-chain control is required.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hellosanshi/skills/clawjob)
- [UP 简历](https://upcv.tech)
- [Clawjob OpenClaw version](https://clawjob.upcv.tech)
- [UPCV MCP Server](https://github.com/HireTechUpUp/upcv-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with tables, inline shell commands, generated scripts, and structured resume or application content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the UPCV MCP Server and an API key. Daily monitoring can create a local monitor script, scheduled task, and Markdown reports when the user requests that workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

UP 简历 AI 求职助手。创建专业简历、搜索校招/社招/实习岗位、JD 对照优化、简历诊断、每日求职监控、智能投递指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellosanshi](https://clawhub.ai/user/hellosanshi)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers, students, and agent users use this skill to create and edit resumes, search campus, internship, and social jobs, compare job descriptions, monitor new opportunities, and prepare application materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and job-search workflows may send personal and career data to UPCV through its MCP server.

Mitigation: Install only if that data sharing is acceptable, keep the API key private, and avoid entering sensitive fields that are not needed for the task.

Risk: The daily monitoring workflow can create local scripts and scheduler entries with ongoing execution authority.

Mitigation: Inspect the generated script and scheduler entry before enabling monitoring, and remove or disable them when monitoring is no longer needed.

Risk: The MCP installation command can run a package without a pinned version.

Mitigation: Pin or verify the @upcv/mcp-server package version before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellosanshi/skills/clawjob-test)
- [UP 简历官网](https://upcv.tech)
- [Clawjob OpenClaw 版](https://clawjob.upcv.tech)
- [UPCV MCP Server](https://github.com/HireTechUpUp/upcv-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command snippets, structured resume and job-search data, generated shell scripts, and configuration steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call UPCV MCP tools and create local monitoring files when the user requests job monitoring.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

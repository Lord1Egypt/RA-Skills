## Description: <br>
Provides agent guidance and scripts for working with Bitrix24 CRM, tasks, calendar, chat, drive, and related REST API workflows using a configured Bitrix24 webhook and MCP documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitrix24](https://clawhub.ai/user/bitrix24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business operators use this skill through an agent to retrieve, summarize, and update Bitrix24 CRM, task, calendar, chat, drive, feed, and team status information. It is intended for portals where a dedicated Bitrix24 webhook has already been configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad automatic access to sensitive CRM, employee, chat, calendar, drive, and feed data through a webhook. <br>
Mitigation: Install only with a dedicated least-privilege Bitrix24 webhook and avoid broad all-module scopes unless that access is intended. <br>
Risk: Implicit invocation can cause Bitrix24 data access when a prompt matches covered business topics. <br>
Mitigation: Consider disabling implicit invocation or requiring explicit Bitrix24 prompts for higher-risk environments. <br>
Risk: Write, delete, feed post, chat message, batch mutation, and scheduled report actions can affect business records or expose information. <br>
Mitigation: Require manual review before any write, delete, feed post, chat message, batch mutation, or scheduled report. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/bitrix24/bitrix24-rest) <br>
- [Bitrix24 Skill Homepage](https://github.com/bitrix24/bitrix24-skill) <br>
- [Bitrix24 MCP Documentation Server](https://mcp-dev.bitrix24.tech/mcp) <br>
- [Access and Auth](references/access.md) <br>
- [MCP Workflow](references/mcp-workflow.md) <br>
- [CRM](references/crm.md) <br>
- [Tasks](references/tasks.md) <br>
- [Calendar](references/calendar.md) <br>
- [Chat and Notifications](references/chat.md) <br>
- [Drive and Disk](references/drive.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Bitrix24 REST endpoints through scripts and return business-facing summaries, tables, or action confirmations.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and CHANGELOG.md, released 2026-04-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

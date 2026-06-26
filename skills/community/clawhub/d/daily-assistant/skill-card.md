## Description: <br>
日常小助手 MCP Server provides daily task management over MCP, including next-task recommendations, task inheritance, overdue checks, daily reviews, and split detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asuranale](https://clawhub.ai/user/asuranale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this MCP server with MCP-compatible agents to manage daily Markdown task files, choose the next task, inherit unfinished work, detect overdue items, and generate daily reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automatic setup creates a local virtual environment, data directory, config.json, and persistent MCP registrations in detected editors. <br>
Mitigation: Review src/setup.py before installation, run the interactive setup for manual control, and back up editor MCP config files before using --auto. <br>
Risk: The MCP tools read daily task files and can write inherited tasks or generated reviews into the configured Markdown data directory. <br>
Mitigation: Use a dedicated task-data directory, confirm config.json points to the intended path, and review generated file changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asuranale/daily-assistant) <br>
- [Project homepage](https://github.com/AsuraNale/daily-assistant-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown returned by MCP tools, with JSON snippets and shell commands in setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese or English responses are controlled by the local config language setting; tools read and write local Markdown task files.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

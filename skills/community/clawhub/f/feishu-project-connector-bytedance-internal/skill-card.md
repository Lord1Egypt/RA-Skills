## Description: <br>
Connects an agent to Meego (Feishu Project, ByteDance internal version) through an MCP service with OAuth authentication to query and manage work items, views, and related project data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wadxm](https://clawhub.ai/user/wadxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized Feishu Project users use this skill to configure OAuth-backed MCP access so an agent can query, create, update, and transition Meego work items and views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote OAuth flow can expose credential file contents to the agent. <br>
Mitigation: Prefer browser OAuth where the agent does not see credential contents; for remote OAuth, verify the file contains only intended fields, avoid logs, and clean up temporary files immediately. <br>
Risk: The connector can create, modify, and transition business work items. <br>
Mitigation: Review each proposed work-item create, modify, or transition action before execution. <br>


## Reference(s): <br>
- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter) <br>
- [Remote OAuth setup documentation](https://bytedance.larkoffice.com/wiki/UspfwpHaFi6LxQkt9xBcIS54nNg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require OAuth credentials stored under ~/.mcporter/credentials.json.] <br>

## Skill Version(s): <br>
1.0.10 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

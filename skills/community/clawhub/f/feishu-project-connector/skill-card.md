## Description:

Connects an agent to Meego (Feishu Project) through an MCP service with OAuth authentication for querying and managing work items, views, and related project data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wadxm](https://clawhub.ai/user/wadxm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Feishu Project can let an agent authenticate through MCP to query to-dos, views, and work items, and assist with creating, updating, or transitioning work items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credential files may be exposed if the remote OAuth proxy flow requires the agent to read or write authorized credentials.

Mitigation: Prefer browser OAuth where possible; when remote OAuth is necessary, require explicit user confirmation, avoid placing credential contents in chat or logs, and keep credentials only in ~/.mcporter/credentials.json.

Risk: Using unpinned npx commands can execute a newer @lark-project/meego-mcporter package than the one reviewed.

Mitigation: Install or invoke a pinned, verified package version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wadxm/skills/feishu-project-connector)
- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter)
- [Feishu Project local authorization documentation](https://project.feishu.cn/b/helpcenter/1ykiuvvj/1n3ae9b4)
- [Feishu Project MCP server endpoint](https://project.feishu.cn/mcp_server/v1)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides OAuth setup and MCP calls; generated outputs may include commands that write or read the local mcporter credential cache.]

## Skill Version(s):

1.0.10 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

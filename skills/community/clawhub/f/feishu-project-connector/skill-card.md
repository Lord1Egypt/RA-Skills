## Description: <br>
Connects agents to Meego (Feishu Project) through an MCP service with OAuth authentication for querying and managing work items, views, and related project data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wadxm](https://clawhub.ai/user/wadxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with Feishu Project/Meego and query or manage project work items, todos, and views through the Meego MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth credentials and may write approved credentials to ~/.mcporter/credentials.json, especially during remote OAuth setup. <br>
Mitigation: Prefer browser OAuth when possible; use the remote credential-copy flow only with explicit user confirmation and keep credentials only in ~/.mcporter/credentials.json. <br>
Risk: The skill relies on installing or running the @lark-project/meego-mcporter npm package. <br>
Mitigation: Confirm trust in the npm package before installing or executing it, and grant only the Feishu Project account permissions needed for the task. <br>


## Reference(s): <br>
- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter) <br>
- [Feishu Project OAuth help](https://project.feishu.cn/b/helpcenter/1ykiuvvj/1n3ae9b4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, the @lark-project/meego-mcporter package, and OAuth credentials managed at ~/.mcporter/credentials.json.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

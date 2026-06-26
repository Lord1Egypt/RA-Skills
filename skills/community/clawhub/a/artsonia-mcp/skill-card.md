## Description: <br>
Access Artsonia student-art portfolios, comments, fans, notification preferences, and artwork downloads through an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent connect to an Artsonia MCP server for linked student artwork portfolios. It supports reviewing portfolios and activity, posting comments, inviting fans, changing notifications, and downloading artwork when the user has supplied Artsonia account credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server requires Artsonia account credentials and can expose linked student portfolio data to an agent. <br>
Mitigation: Install only when the user is comfortable granting that access, keep credentials scoped to the intended account, and avoid sharing credential-bearing configuration. <br>
Risk: Some tools can post comments, invite fans, change notifications, or download artwork to disk. <br>
Mitigation: Confirm intent before using write, invitation, notification, or download tools, and review downloaded files and manifests before further sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chrischall/artsonia-mcp) <br>
- [artsonia-mcp npm package](https://www.npmjs.com/package/artsonia-mcp) <br>
- [Artifact-linked source repository](https://github.com/chrischall/artsonia-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Artsonia credentials and an installed MCP server; agent use may access student portfolio data or perform account actions.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

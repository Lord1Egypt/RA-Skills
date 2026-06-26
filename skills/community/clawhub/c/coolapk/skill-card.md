## Description: <br>
酷安社区搜索工具 - 搜索帖子、用户、应用、话题信息，并通过 CLI 输出精简 JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lniosy](https://clawhub.ai/user/lniosy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code can search and browse Coolapk community content through the coolapk CLI, including posts, users, apps, topics, feeds, and notifications. Logged-in users can also use it for account actions such as likes, replies, follows, and unfollows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to pass a Coolapk account cookie to the CLI, which can expose account credentials if copied into logs, shell history, or shared transcripts. <br>
Mitigation: Use an isolated environment, avoid long-lived cookies in shell commands, and rotate or revoke the cookie after use. <br>
Risk: Logged-in commands can change account state through likes, replies, follows, and unfollows. <br>
Mitigation: Require explicit approval before account-changing actions and review the target post, user, or reply before execution. <br>
Risk: The release depends on the third-party coolapk-mcp Python package. <br>
Mitigation: Review and trust the package before installation, and install it in an isolated Python environment. <br>


## Reference(s): <br>
- [Coolapk MCP dependency](https://github.com/lniosy/coolapk-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/lniosy/coolapk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and compact JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands omit empty JSON fields to reduce agent context usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

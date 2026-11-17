## Description:

酷安社区搜索工具 — 搜索帖子、用户、应用、话题信息（CLI 直调，比 MCP Server 更省 token）

This skill is ready for commercial/non-commercial use.

## Publisher:

[lniosy](https://clawhub.ai/user/lniosy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent search and browse Coolapk posts, users, applications, topics, home feeds, and notifications through the Coolapk CLI. With login, the agent can also prepare account actions such as likes, replies, follows, and unfollows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external coolapk-mcp Python package that is not pinned in the artifact.

Mitigation: Review and pin a vetted package version before managed deployment.

Risk: Cookie login and account-changing commands can act through the user's Coolapk account.

Mitigation: Treat cookies as passwords and review reply, like, follow, and unfollow commands before execution.

Risk: The artifact documents local Coolapk configuration under ~/.coolapk-mcp/config.json.

Mitigation: Protect local configuration files and avoid sharing session or device data in transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lniosy/skills/coolapk)
- [coolapk-mcp dependency](https://github.com/lniosy/coolapk-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; Coolapk CLI commands return compact JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output omits empty fields to reduce token use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

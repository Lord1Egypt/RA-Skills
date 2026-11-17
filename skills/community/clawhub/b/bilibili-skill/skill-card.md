## Description:

Bilibili Skill helps an agent use Bilibili CLI and MCP workflows to publish or delete dynamics, inspect videos and users, search content, query live rooms, and retrieve danmaku.

This skill is for research and development only.

## Publisher:

[osskn4w7](https://clawhub.ai/user/osskn4w7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate Bilibili search, lookup, live-room, danmaku, and account actions through CLI commands or MCP configuration. The evidence recommends cautious learning and testing use because the skill can act on a Bilibili account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Bilibili account cookies and can perform account-changing actions.

Mitigation: Use an account approved for automation, keep cookies out of shared workspace files when possible, and require explicit user approval before posting, deleting, reposting, or liking content.

Risk: Install examples include system Python package installation with --break-system-packages.

Mitigation: Install dependencies in an isolated virtual environment instead of modifying system Python.

Risk: Batch examples use shell=True and may encourage unsafe command composition.

Mitigation: Use argument arrays or carefully quoted command construction, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/osskn4w7/skills/bilibili-skill)
- [bilibili-api Python library](https://github.com/Nemo2011/bilibili-api)
- [Bilibili MCP server reference](https://github.com/huccihuang/bilibili-mcp-server)
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bilibili CLI or MCP configuration guidance and JSON-output command options.]

## Skill Version(s):

1.0.0 (source: server release metadata and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

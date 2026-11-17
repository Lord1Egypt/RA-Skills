## Description:

Fragments helps agents capture, search, update, delete, and comment on Memos records and maintain structured daily work logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hx-w](https://clawhub.ai/user/hx-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage personal or workspace Memos notes, comments, and daily work journals through confirmable agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Memos access may expose private notes, comments, or work logs to the agent.

Mitigation: Install only when authenticated agent access to Memos data is acceptable, and prefer project-scoped setup where possible.

Risk: Plaintext Personal Access Token storage can increase credential exposure if local config files are broadly readable.

Mitigation: Store the PAT in a secret manager or a tightly permissioned local file, and never echo it in conversation.

Risk: Optional post-task hooks can prompt daily-log workflows after agent sessions and may affect user control expectations.

Mitigation: Skip optional hooks unless automatic daily-log prompts are explicitly desired, and review any MCP or agent configuration changes before applying them.

## Reference(s):

- [Daily Log](references/daily-log.md)
- [Memo Capture](references/memo-capture.md)
- [Memo Comments](references/memo-comments.md)
- [Search Strategy](references/search-strategy.md)
- [Setup - Claude Code](references/setup-claude-code.md)
- [Setup - OpenCode](references/setup-opencode.md)
- [Setup - OpenClaw](references/setup-openclaw.md)
- [Memos Docker Image](https://hub.docker.com/repository/docker/deepshape/memos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands, JSON configuration, and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ranked JSON search results when using the optional local reranker.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

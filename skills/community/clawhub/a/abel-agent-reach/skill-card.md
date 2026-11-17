## Description:

Agent Reach helps agents search, read, and interact with web and social platforms including X, Reddit, YouTube, GitHub, Bilibili, Xiaohongshu, Douyin, Weibo, WeChat Articles, LinkedIn, Instagram, RSS, SkillBoss API Hub, and arbitrary web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent broad web and social-platform research reach, including reading URLs, searching web and platform content, fetching transcripts or metadata, checking GitHub resources, and configuring platform channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, URLs, and page content may be sent to external scraping or search services.

Mitigation: Require explicit approval before sending private, internal, sensitive, or account-specific URLs or queries to external services.

Risk: Some supported channels rely on logged-in sessions, browser cookies, or imported cookies.

Mitigation: Use dedicated low-privilege accounts and avoid default browser cookies unless the user understands the account-access risk.

Risk: The skill includes write-capable social actions such as publishing, posting, or commenting.

Mitigation: Require user confirmation for any action that posts, comments, publishes, changes account state, or interacts with another user.

Risk: Setup guidance can involve installing packages, fetching mutable instructions, or configuring proxies.

Mitigation: Review install commands and proxy settings before execution, and prefer pinned or trusted sources where possible.

## Reference(s):

- [Agent Reach homepage](https://github.com/Panniantong/Agent-Reach)
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)
- [ClawHub Agent Reach listing](https://clawhub.ai/abeltennyson/skills/abel-agent-reach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls and platform-tool commands that require credentials, cookies, or user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

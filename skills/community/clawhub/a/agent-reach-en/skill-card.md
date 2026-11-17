## Description:

Agent Reach helps an AI agent install, configure, and use upstream tools for web and social platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, LinkedIn, Boss Zhipin, WeChat Official Accounts, RSS, and general web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverchenx](https://clawhub.ai/user/neverchenx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Agent Reach to set up platform access channels, check channel availability, and route web or social-media retrieval tasks through upstream command-line and MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to install mutable remote software from an upstream archive.

Mitigation: Install only from trusted sources, review what the installer changes, and prefer a sandboxed environment before use.

Risk: The skill handles platform cookies and authenticated accounts across multiple services.

Mitigation: Use dedicated secondary accounts, avoid sharing primary-account cookies in chat, and store credentials only in the intended local configuration location.

Risk: Some upstream tools can post, publish, configure proxies, extract cookies, or make persistent configuration changes.

Mitigation: Require explicit user confirmation before any posting action, cookie extraction, proxy configuration, or persistent config change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neverchenx/skills/agent-reach-en)
- [Agent Reach upstream install archive](https://github.com/Panniantong/agent-reach/archive/main.zip)
- [Cookie-Editor Chrome extension](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup commands, channel status guidance, cookie-handling instructions, proxy configuration guidance, and upstream tool invocation examples.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

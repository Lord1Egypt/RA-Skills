## Description:

Edison Agent Reach guides agents to search, read, and interact with web pages and supported platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn, Boss Zhipin, RSS, and Exa web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edisonchenai](https://clawhub.ai/user/edisonchenai)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to research online information, inspect shared platform URLs, operate supported platform search and read tools, and configure platform channels when needed. The skill also covers account-bound platform interactions such as posting or commenting where supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can involve logged-in platform sessions, cookies, or account-bound services.

Mitigation: Use only reviewed credentials and require explicit user confirmation before cookie use or account-bound access.

Risk: The skill includes workflows that may publish, comment, or otherwise change public or account-bound platform state.

Mitigation: Require an explicit preview and user confirmation before any publish, comment, or other mutating platform action.

Risk: Setup workflows may rely on package installation, Docker operations, proxy changes, anti-bot workarounds, or mutable online instructions.

Mitigation: Review setup steps before execution, prefer pinned or locally reviewed instructions, and confirm before package installation, Docker use, proxy changes, or anti-bot workarounds.

## Reference(s):

- [Edison Agent Reach ClawHub Skill Page](https://clawhub.ai/edisonchenai/skills/edison-agent-reach)
- [Agent Reach Install Guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown usage guidance with shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may depend on platform credentials, cookies, proxies, and installed third-party tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

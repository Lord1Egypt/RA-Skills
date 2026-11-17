## Description:

Use the internet to search, read, and interact with supported platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn, Boss Zhipin, RSS, Exa web search, and general web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-owo](https://clawhub.ai/user/lulu-owo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to direct an agent through web research, platform-specific reading, posting or interaction workflows, and setup checks for upstream tools. It is most relevant when an agent needs command-level guidance for search, content retrieval, transcripts, social platforms, RSS feeds, or channel configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can automatically copy browser login cookies, which should be treated as account credentials.

Mitigation: Review the setup path before installing, prefer safe or dry-run mode, and avoid automatic browser-cookie import unless the user intentionally authorizes reading active sessions.

Risk: The skill can install mutable external tools and use remote setup or update paths.

Mitigation: Review global installs and remote update commands before execution, and pin or inspect upstream packages where operational controls require reproducibility.

Risk: Docker and MCP services may expand the local execution and network surface during channel setup.

Mitigation: Run services in a constrained environment, expose only required local ports, and avoid passing unnecessary cookies, API keys, or proxy credentials to those services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lulu-owo/skills/agent-reach-skip)
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)
- [Exa setup guide](artifact/agent_reach/guides/setup-exa.md)
- [Twitter setup guide](artifact/agent_reach/guides/setup-twitter.md)
- [Reddit setup guide](artifact/agent_reach/guides/setup-reddit.md)
- [XiaoHongShu setup guide](artifact/agent_reach/guides/setup-xiaohongshu.md)
- [WeChat setup guide](artifact/agent_reach/guides/setup-wechat.md)
- [Groq setup guide](artifact/agent_reach/guides/setup-groq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, URLs, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to run upstream CLIs, MCP tools, Docker services, browser-cookie import, and platform-specific setup checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

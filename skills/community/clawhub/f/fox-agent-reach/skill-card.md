## Description:

Searches and reads content across Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, Weibo, WeChat Articles, LinkedIn, Instagram, RSS, Exa web search, and general web pages, with setup guidance for supported channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinthqod](https://clawhub.ai/user/qinthqod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when they need an agent to search, read, summarize, or configure access to supported web and social platforms. It is also used when a user provides a supported platform URL or requests public posting, commenting, or other account interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad web access can send agent requests to many third-party platforms and services.

Mitigation: Review requested destinations before execution and restrict access to the minimum platforms needed for the user task.

Risk: Authenticated channels may require cookies or browser-derived credentials.

Mitigation: Use a dedicated browser profile or scoped cookie file, avoid normal browser profiles, and keep credentials limited to the intended channel.

Risk: Posting, commenting, or other account interactions can create public or persistent changes.

Mitigation: Require an explicit preview and user confirmation before any post, comment, publish, or account action.

Risk: Remote setup instructions and global package installs can change the local environment.

Mitigation: Review remote setup guides before following them, prefer scoped or isolated installs, and avoid global package installation where practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinthqod/skills/fox-agent-reach)
- [Agent Reach homepage](https://github.com/Panniantong/Agent-Reach)
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose web requests, local tool commands, channel setup steps, and account interaction workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

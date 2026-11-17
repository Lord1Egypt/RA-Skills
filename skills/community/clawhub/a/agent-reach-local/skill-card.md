## Description:

Gives an AI agent commands and setup guidance to search, read, and interact with web, social, video, code, RSS, and article sources across multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larry-at](https://clawhub.ai/user/larry-at)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let an agent retrieve information from supported online platforms, inspect shared URLs, run searches, and configure platform-specific channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to access social platforms, web services, and third-party readers using cookies, profiles, proxies, or login setup.

Mitigation: Require explicit user approval before cookie use, login setup, proxy configuration, browser-profile access, or third-party URL reader use.

Risk: Some setup paths rely on mutable remote instructions or package installation commands.

Mitigation: Review fetched install instructions and package commands before execution, and prefer isolated environments for new tools.

Risk: The skill includes commands for public posting or interaction on supported platforms.

Mitigation: Require explicit approval for each posting, commenting, publishing, or other account-affecting action.

## Reference(s):

- [Agent Reach Homepage](https://github.com/Panniantong/Agent-Reach)
- [Agent Reach Install Guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform-specific commands, setup steps, diagnostics, API/tool calls, and content retrieval guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

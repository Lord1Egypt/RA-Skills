## Description: <br>
Agent Reach.Bak helps an agent search, read, and interact with web and social platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, Weibo, WeChat Articles, LinkedIn, Instagram, RSS, Exa web search, and arbitrary web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reiy-leo](https://clawhub.ai/user/reiy-leo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to gather online information, read linked content, inspect platform-specific resources, configure supported channels, and perform guarded social-platform actions when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cookie-based account access and posting-capable commands can expose accounts or change account state. <br>
Mitigation: Use secondary accounts or read-only workflows where possible, avoid sharing main-account cookies casually, and require explicit preview and confirmation before any post, comment, upload, or account-changing action. <br>
Risk: The skill directs agents to inspect a remote install guide before setup, so installation steps may affect the local environment. <br>
Mitigation: Review the remote install guide before running setup commands and only proceed with commands that match the intended channel configuration. <br>


## Reference(s): <br>
- [Agent Reach homepage](https://github.com/Panniantong/Agent-Reach) <br>
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>
- [ClawHub skill page](https://clawhub.ai/reiy-leo/agent-reach-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, URLs, and platform-specific guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON returned by platform tools or command-line utilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

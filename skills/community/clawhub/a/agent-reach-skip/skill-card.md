## Description: <br>
Use the internet to search, read, and interact with 13+ platforms, including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn, Boss Zhipin, RSS, Exa web search, and web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulu-owo](https://clawhub.ai/user/lulu-owo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route web research, social-platform reading, account interaction, and channel setup requests across supported platform tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can change the host system by installing packages or tools. <br>
Mitigation: Review the setup path before execution, prefer safe or dry-run mode first, and use an isolated environment for installation. <br>
Risk: Cookie import and credential configuration can read or store browser session cookies and API keys. <br>
Mitigation: Avoid automatic browser-cookie import unless the affected accounts are understood, provide only required credentials, and protect the local Agent Reach configuration. <br>
Risk: Supported tools can post, comment, publish, or otherwise interact with user accounts. <br>
Mitigation: Require explicit user confirmation before posting, commenting, publishing, or performing other account actions. <br>


## Reference(s): <br>
- [Agent Reach.Skip ClawHub page](https://clawhub.ai/lulu-owo/agent-reach-skip) <br>
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>
- [Exa setup guide](agent_reach/guides/setup-exa.md) <br>
- [Twitter setup guide](agent_reach/guides/setup-twitter.md) <br>
- [Reddit setup guide](agent_reach/guides/setup-reddit.md) <br>
- [WeChat setup guide](agent_reach/guides/setup-wechat.md) <br>
- [XiaoHongShu setup guide](agent_reach/guides/setup-xiaohongshu.md) <br>
- [Groq Whisper setup guide](agent_reach/guides/setup-groq.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and tool/API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command sequences for package installation, browser-cookie configuration, proxy setup, and platform-specific API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

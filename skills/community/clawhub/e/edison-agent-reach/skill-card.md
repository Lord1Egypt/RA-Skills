## Description: <br>
Use the internet to search, read, and interact with web pages and supported platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn, Boss Zhipin, RSS, and Exa web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdisonChenAI](https://clawhub.ai/user/EdisonChenAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to search online sources, read URLs and platform content, retrieve transcripts or feeds, interact with supported platforms, and configure platform channels when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use account cookies or browser profiles for logged-in platform access. <br>
Mitigation: Use isolated browser profiles or test accounts, avoid valuable account cookies, and review access before configuring any channel. <br>
Risk: The skill can post, comment, publish, or otherwise change account state on supported platforms. <br>
Mitigation: Require explicit user confirmation before any posting, commenting, publishing, or account-changing action. <br>
Risk: Setup instructions are fetched from a mutable remote install guide and helper code. <br>
Mitigation: Review the remote install guide and helper code before setup, and pin or archive trusted setup instructions for controlled deployments. <br>
Risk: Some workflows involve anti-bot bypass tooling. <br>
Mitigation: Avoid anti-bot bypass workflows unless they are authorized and consistent with the target platform's terms and the user's policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EdisonChenAI/edison-agent-reach) <br>
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, curl, and API-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to call local platform tools, use /tmp for temporary output, diagnose channels with agent-reach doctor, and configure channels that can require cookies or browser profiles.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Agent Reach helps an AI agent install and configure upstream tools for Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, LinkedIn, Boss Zhipin, WeChat Official Accounts, RSS, and web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeverChenX](https://clawhub.ai/user/NeverChenX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up and check platform access channels, then call upstream tools directly for web, social, video, repository, job, RSS, and article retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports broad social and web automation, including posting, commenting, liking, and proxy changes. <br>
Mitigation: Require explicit user confirmation before any write action, engagement action, proxy change, or platform automation that could affect an account. <br>
Risk: The skill asks users to provide or extract login cookies for some platforms. <br>
Mitigation: Use dedicated secondary accounts, avoid pasting raw cookies into chat, and review stored files under ~/.agent-reach before and after setup. <br>
Risk: Some examples involve anti-bot or blocked-IP workarounds. <br>
Mitigation: Confirm the user is authorized to access the target service and avoid bypass steps that violate platform terms or user intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NeverChenX/agent-reach-en) <br>
- [Agent Reach upstream package archive](https://github.com/Panniantong/agent-reach/archive/main.zip) <br>
- [Cookie-Editor Chrome extension](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for installing tools, configuring cookies or proxies, running diagnostics, and invoking upstream CLIs or MCP tools.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

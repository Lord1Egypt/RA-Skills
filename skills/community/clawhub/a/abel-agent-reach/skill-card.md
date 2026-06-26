## Description: <br>
Agent Reach helps an AI agent search, read, and interact with web and social platforms including Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, Weibo, WeChat Articles, LinkedIn, Instagram, RSS, SkillBoss API Hub, and arbitrary web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use Agent Reach to give an agent web research, page-reading, platform search, and supported social interaction workflows across many online channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad API-backed web access and scraping capability. <br>
Mitigation: Review each requested web access task before execution, scope searches and scraping to the user's stated goal, and avoid collecting sensitive or unnecessary data. <br>
Risk: Some channels may require logged-in cookies, browser sessions, or account credentials. <br>
Mitigation: Require explicit approval before cookie import or logged-in session use, store only the minimum required credentials, and remove credentials when the task is complete. <br>
Risk: The skill can guide proxy changes, installs, and anti-bot browser automation. <br>
Mitigation: Require explicit approval before proxy changes, package installs, browser automation setup, or anti-bot workflows, and prefer temporary output locations for generated files. <br>
Risk: Supported platform commands include posting, commenting, or other public interactions. <br>
Mitigation: Require explicit user confirmation immediately before any post, comment, publish, or other public-facing action, including a preview of the exact content and target account or platform. <br>


## Reference(s): <br>
- [Agent Reach ClawHub Page](https://clawhub.ai/abeltennyson/abel-agent-reach) <br>
- [Agent Reach Homepage](https://github.com/Panniantong/Agent-Reach) <br>
- [Agent Reach Install Guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, and API-call examples; many channel commands return JSON or markdown content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for SkillBoss API Hub features; some channels may require cookies, proxies, browser sessions, installed CLIs, or user approval for public interactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

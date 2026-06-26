## Description: <br>
AI领域日报生成工具，支持飞书机器人消息格式；当用户需要生成AI行业日报、整理AI动态或分析AI资讯时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c1028874817-beep](https://clawhub.ai/user/c1028874817-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and team operators use this skill to collect, verify, and summarize AI industry updates from the past 24 hours into a concise daily report suitable for Feishu bot messages or Markdown chat output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated daily reports may include unverified or outdated AI news if sources are not checked carefully. <br>
Mitigation: Use authoritative sources, cross-check important claims across multiple sources, cite source links, and mark sections with no major activity as unavailable rather than guessing. <br>
Risk: Deploying the skill as a Feishu bot can expose chat content, API keys, or webhook endpoints to external services. <br>
Mitigation: Confirm what data is sent to Coze, Dify, OpenAI, Claude, or other providers; protect API keys; implement Feishu signature verification; avoid ngrok in production; and add rate limits and logging controls. <br>


## Reference(s): <br>
- [AI日报信息来源清单](references/sources.md) <br>
- [AI日报Skill部署指南](deploy-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/c1028874817-beep/ai-daily-report-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or Feishu rich-text-ready message content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Direct chat output only; the skill instructs the agent not to create report files and suggests a 3000-4000 character message length.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

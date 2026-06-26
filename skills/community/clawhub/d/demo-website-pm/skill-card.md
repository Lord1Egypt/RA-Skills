## Description: <br>
面向零技术用户，把网站 / 小程序 demo 需求拆成产品需求、设计需求、技术需求三份文档，并配合 GitHub 与 Vercel / 微信小程序开发工具直接上线部署。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[jhc888007](https://clawhub.ai/user/jhc888007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Non-technical users use this skill to turn a demo website or WeChat mini program idea into product, design, and technical requirement documents for a coding agent. It also guides local runs, GitHub upload, Vercel deployment, and WeChat Developer Tools preview or test release in small step-by-step interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose .env files, database URLs, API keys, tokens, passwords, private keys, or unredacted screenshots while following setup and deployment steps. <br>
Mitigation: Keep secrets out of chat and GitHub, enter them only in official Vercel, WeChat, Cursor, or local configuration screens, and rotate anything accidentally exposed. <br>
Risk: The skill is intended for demo planning and deployment guidance, so its outputs may not meet production reliability, security, or compliance expectations. <br>
Mitigation: Use the generated documents and setup steps for demos and idea validation, then perform separate production review before relying on the resulting application. <br>


## Reference(s): <br>
- [Cursor 与编辑器准备](reference/cursor-and-editor-setup.md) <br>
- [Frontend Design](reference/frontend-design.md) <br>
- [GitHub 入门引导](reference/github-onboarding.md) <br>
- [本地环境排错](reference/local-env-troubleshooting.md) <br>
- [非技术用户沟通风格](reference/non-tech-communication-style.md) <br>
- [Vercel 部署引导](reference/vercel-onboarding.md) <br>
- [微信小程序真机预览与上线体验指南](reference/wechat-miniprogram-onboarding.md) <br>
- [微信开发者工具与小程序注册指南](reference/wechat-miniprogram-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jhc888007/demo-website-pm) <br>
- [GitHub Docs](https://docs.github.com/) <br>
- [Vercel Docs](https://vercel.com/docs) <br>
- [WeChat Developer Tools Download](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance and requirement documents with occasional inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; the skill tells the agent not to output business code.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

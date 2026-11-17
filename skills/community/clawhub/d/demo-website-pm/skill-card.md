## Description:

面向零技术用户，把网站 / 小程序 demo 需求拆成产品需求、设计需求、技术需求三份文档，并配合 GitHub 与 Vercel / 微信小程序开发工具 直接上线部署

This skill is for demonstration purposes and not for production usage.

## Publisher:

[jhc888007](https://clawhub.ai/user/jhc888007)

### License/Terms of Use:

MIT-0

## Use Case:

Non-technical users and agents use this skill to plan a website or WeChat mini-program demo, produce product/design/technical requirement documents, and receive step-by-step guidance for local runs, GitHub upload, Vercel deployment, or WeChat developer-tool preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated requirements may permit plaintext password handling in demo authentication flows.

Mitigation: Require generated requirements to forbid plaintext password storage and use appropriate password hashing even for demos.

Risk: Beginner users may run package installation or deployment steps without reviewing dependencies or build behavior.

Mitigation: Review dependencies before npm or pip installation and pause on unfamiliar install scripts, permission prompts, or deployment errors.

Risk: Users may accidentally publish secrets, passwords, AppIDs, environment IDs, or private project details during GitHub, Vercel, or WeChat upload.

Mitigation: Confirm what will become public before upload, keep secrets in local or platform environment variables, and avoid sharing real passwords or unnecessary account identifiers in chat or repositories.

## Reference(s):

- [Skill page](https://clawhub.ai/jhc888007/skills/demo-website-pm)
- [Cursor and editor setup](artifact/reference/cursor-and-editor-setup.md)
- [Frontend design](artifact/reference/frontend-design.md)
- [GitHub onboarding](artifact/reference/github-onboarding.md)
- [Local environment troubleshooting](artifact/reference/local-env-troubleshooting.md)
- [Non-technical user communication style](artifact/reference/non-tech-communication-style.md)
- [Vercel onboarding](artifact/reference/vercel-onboarding.md)
- [WeChat mini-program onboarding](artifact/reference/wechat-miniprogram-onboarding.md)
- [WeChat mini-program setup](artifact/reference/wechat-miniprogram-setup.md)
- [GitHub Docs](https://docs.github.com/)
- [Vercel Docs](https://vercel.com/docs)
- [WeChat Developer Tools](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown prose with step-by-step instructions, requirements documents, and occasional inline shell command or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not directly produce business application code; focuses on planning documents and beginner-friendly execution guidance.]

## Skill Version(s):

1.0.15 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

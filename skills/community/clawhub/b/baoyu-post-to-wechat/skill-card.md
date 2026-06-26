## Description: <br>
Posts content to WeChat Official Account via API or Chrome CDP, supporting article publishing from HTML, markdown, or plain text and image-text posting with multiple images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to prepare and publish WeChat Official Account drafts from markdown, HTML, plain text, or image collections. It helps agents guide setup, choose API or browser workflows, configure account preferences, and report publishing results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat login material, API credentials, browser sessions, clipboard input, and local preference files. <br>
Mitigation: Use a dedicated browser profile and WeChat account context, keep .env and EXTEND.md private, and review permissions before running publishing workflows. <br>
Risk: Telegram QR forwarding can expose a login handoff if the bot or chat is not controlled by the user. <br>
Mitigation: Enable Telegram QR forwarding only with a bot and chat the user fully controls, and remove related tokens when forwarding is not needed. <br>
Risk: Remote SSH publishing can route publishing traffic through a remote host. <br>
Mitigation: Use remote publishing only with trusted SSH hosts, key-based authentication, and known host verification, or use local API/browser publishing when remote routing is unnecessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-post-to-wechat) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat) <br>
- [API Credential Setup](references/api-setup.md) <br>
- [Article Posting](references/article-posting.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Image-Text Posting](references/image-text-posting.md) <br>
- [Multi-Account Support](references/multi-account.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, HTML, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated content files, configuration values, and publishing status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local markdown or HTML publishing inputs and may invoke WeChat API, browser automation, clipboard, or SSH-based remote publishing workflows depending on user configuration.] <br>

## Skill Version(s): <br>
1.118.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

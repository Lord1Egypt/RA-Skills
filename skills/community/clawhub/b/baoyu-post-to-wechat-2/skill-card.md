## Description: <br>
Posts content to WeChat Official Account via API or Chrome CDP, supporting article publishing from HTML, Markdown, or plain text and image-text posts with multiple images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare and post WeChat Official Account drafts from Markdown, HTML, plain text, and image sets while managing account-specific publishing preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat account credentials and browser login sessions. <br>
Mitigation: Install only from a trusted publisher, inspect EXTEND.md and .baoyu-skills/.env before use, avoid committing secrets, and prefer a dedicated Chrome profile. <br>
Risk: Browser mode can control Chrome, clipboard content, and draft creation. <br>
Mitigation: Confirm the selected account and article content before execution, and treat browser automation as capable of making changes in the active WeChat session. <br>
Risk: The security summary notes that one browser article path saves drafts even though help text implies draft saving is optional. <br>
Mitigation: Review the chosen article workflow before use and verify whether it will create or save a draft. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nengnengZ/baoyu-post-to-wechat-2) <br>
- [OpenClaw homepage metadata](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com) <br>
- [Article posting reference](references/article-posting.md) <br>
- [Image-text posting reference](references/image-text-posting.md) <br>
- [First-time setup reference](references/config/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and publishing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local preference files, credential environment entries, converted article HTML, and WeChat draft content.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.56.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

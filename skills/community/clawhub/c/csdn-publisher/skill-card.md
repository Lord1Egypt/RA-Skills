## Description: <br>
Writes technical articles and publishes them to CSDN using browser automation, QR-code login, optional Telegram delivery for login QR codes, and a Chinese technical-blog writing style guide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c4chuan](https://clawhub.ai/user/c4chuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical writers use this skill to draft Chinese technical blog posts, review them with the user, and publish approved articles to a CSDN account. It also supports QR-code login, article injection, retry guidance, and duplicate checks for news-style posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a live CSDN account through QR login, saved cookies, and browser automation. <br>
Mitigation: Install it only when an agent should operate that CSDN account, review final article content before publishing, and protect or delete saved cookies and QR images after use. <br>
Risk: Optional Telegram notification can send login QR codes to the wrong destination if configured incorrectly. <br>
Mitigation: Verify the Telegram target before sending QR codes or login notifications. <br>
Risk: Optional Notion duplicate checks require access to a Notion database. <br>
Mitigation: Use a Notion token scoped only to the intended database and confirm duplicate-check results before skipping or publishing news items. <br>


## Reference(s): <br>
- [CSDN Publisher ClawHub release](https://clawhub.ai/c4chuan/csdn-publisher) <br>
- [CSDN Markdown editor](https://editor.csdn.net/md) <br>
- [CSDN login](https://passport.csdn.net/login) <br>
- [Notion database query API](https://api.notion.com/v1/databases/$DATABASE_ID/query) <br>
- [Telegram Bot API message endpoint](https://api.telegram.org/bot{bot_token}/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, shell-command snippets, browser workflow steps, and publishing status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local draft files, login QR images, saved CSDN session cookies, and optional duplicate-check results.] <br>

## Skill Version(s): <br>
2.3.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

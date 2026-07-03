## Description: <br>
Accepts files, folders, URLs, or ideas, generates polished HTML, converts it for WeChat compatibility, and publishes it to a WeChat Official Account draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lutongsuo](https://clawhub.ai/user/lutongsuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operators use this skill to transform source material into a WeChat-ready article and send it to their WeChat Official Account draft box for review and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can read broad user-provided files or URLs and automatically upload generated content to WeChat. <br>
Mitigation: Run it only on intended inputs and review the generated HTML and cover image before publishing from the WeChat draft box. <br>
Risk: The workflow uses WeChat Official Account credentials and may install Python packages at runtime. <br>
Mitigation: Use a constrained environment, provide credentials only for the session, and install or review dependencies before running the publishing step. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lutongsuo/skills/anything-to-wechat) <br>
- [README](README.md) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML/image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-provided files or URLs, convert HTML for WeChat, generate a cover image, and upload content to a WeChat draft box using user-provided credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

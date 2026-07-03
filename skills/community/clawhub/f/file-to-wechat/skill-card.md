## Description: <br>
Converts files such as PDFs, Word documents, spreadsheets, slides, images, audio, and web pages into Markdown, generates WeChat-compatible HTML and a cover image, and uploads the result to a WeChat Official Account draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lutongsuo](https://clawhub.ai/user/lutongsuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and WeChat Official Account publishers use this skill to turn source files or URLs into styled WeChat articles and create draft posts for review in the WeChat platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad user-selected files and generate derivative article content. <br>
Mitigation: Use it only with files intended for publication, avoid sensitive documents unless publication is deliberate, and review generated Markdown, HTML, and cover images before continuing. <br>
Risk: The skill can upload generated content to a WeChat Official Account draft box using account credentials without a clear consent checkpoint in the artifact workflow. <br>
Mitigation: Confirm the target account and publication intent before upload, keep credentials in environment variables, and review the resulting draft in WeChat before publishing. <br>
Risk: Cloud fallback conversion can send document content to an external Markdown conversion service. <br>
Mitigation: Prefer local MarkItDown conversion for private documents and use the cloud fallback only when the user accepts external processing. <br>
Risk: Runtime dependency installation may change the execution environment. <br>
Mitigation: Preinstall and review required Python packages before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lutongsuo/skills/file-to-wechat) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell commands, plus generated Markdown, HTML, image, and WeChat draft artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires selected source-file access, WeChat Official Account credentials, local Python dependencies, and the anything-to-wechat companion skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

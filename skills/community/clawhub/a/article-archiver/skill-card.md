## Description: <br>
Archives web, Twitter/X, and WeChat articles into Feishu documents while preserving formatting, images, metadata, duplicate checks, and success or failure notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yemoo](https://clawhub.ai/user/yemoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and knowledge workers use this skill to save shared article links into an organized Feishu knowledge base with extracted content, images, source metadata, duplicate detection, and completion notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Feishu and Twitter/X credentials may expose account or workspace access. <br>
Mitigation: Replace and rotate bundled credentials before installation, and keep secrets outside the skill artifact. <br>
Risk: Automatic archiving can send shared links and extracted content to fixed Feishu locations and a fixed notification recipient. <br>
Mitigation: Confirm the Feishu destination and notification recipient before use, and require explicit user confirmation before archiving shared links. <br>
Risk: Shell-based helpers may be unsafe when processing untrusted URLs or article content. <br>
Mitigation: Review and fix shell-command construction, URL validation, and quoting before using the skill with untrusted inputs. <br>


## Reference(s): <br>
- [Article Archiver on ClawHub](https://clawhub.ai/yemoo/article-archiver) <br>
- [Feishu archive format reference](https://qingzhao.feishu.cn/wiki/ZVCFwN7bci1uyhknLpucA18FnSe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and JavaScript command examples; runtime output is archived Feishu content and notification text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archives may include extracted article text, images, metadata, duplicate-status messages, and Feishu document links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

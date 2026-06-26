## Description: <br>
Converts Feishu document or Wiki links into Xiaohongshu-ready image posts, producing 1242x1660 vertical cards, draft post copy, title options, hashtags, and a Feishu document link for publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developers use this skill to transform Feishu documents or Wiki pages into Xiaohongshu posts with rendered cards, social copy, title options, hashtags, and a Feishu document package for review and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports exposed Feishu credentials and default upload through a fixed Feishu account. <br>
Mitigation: Remove embedded credentials, rotate the exposed secret, and require caller-provided scoped FEISHU_APP_ID, FEISHU_APP_SECRET, and FEISHU_OWNER_ID before use. <br>
Risk: The skill can process and upload source document content to Feishu. <br>
Mitigation: Do not run it on confidential documents unless the credential issue is remediated and the destination account, permissions, and generated document contents are reviewed. <br>


## Reference(s): <br>
- [Design Styles Reference](references/design-styles.md) <br>
- [ClawHub Release Page](https://clawhub.ai/xiaohuaishu/feishu-xhs-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell commands, plus generated HTML/PNG card files and Feishu document links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1242x1660 image cards and can package generated images, summary copy, titles, and hashtags into a Feishu document.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

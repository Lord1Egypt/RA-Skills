## Description: <br>
获取飞书云文档内容，返回文档的 Markdown 内容，并标出需要通过配套工具单独下载的图片、文件和画板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read Feishu/Lark cloud document content from a document URL or token as Markdown. It is also used to identify embedded media tokens and route wiki links to the correct Feishu tool based on resolved object type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched Feishu/Lark document text and downloaded attachments may contain sensitive business data. <br>
Mitigation: Use least-privilege Feishu permissions, provide explicit document or wiki links/tokens, and choose media download paths carefully. <br>
Risk: Wiki links can refer to different Feishu object types, not only cloud documents. <br>
Mitigation: Resolve wiki tokens with feishu_wiki_space_node before selecting the Feishu tool for the underlying object type. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/feishu-doc-read) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown with embedded HTML-style media placeholders and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include image, file, and whiteboard tokens that require separate media download handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

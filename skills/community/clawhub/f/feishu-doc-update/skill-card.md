## Description: <br>
更新飞书云文档，支持追加、覆盖、定位替换、全文替换、前后插入和删除等 7 种更新模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent update Feishu cloud documents by appending, replacing, inserting, deleting, or renaming document content with precise text- or heading-based targeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete content in Feishu cloud documents. <br>
Mitigation: Confirm the account, workspace, document, mode, and target range before use, especially for overwrite, replace_all, and delete_range. <br>
Risk: Broad overwrite or replacement operations can remove content that may be difficult to reconstruct, such as images, comments, or embedded objects. <br>
Mitigation: Prefer small, precise local updates with replace_range, append, insert_before, or insert_after, and avoid overwrite unless the document is intentionally being rebuilt. <br>
Risk: Repeated or ambiguous target text can cause edits to affect the wrong location. <br>
Mitigation: Use unique text ranges or heading-based selection with enough context to identify the intended section. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/feishu-doc-update) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown document content and JSON operation status or error responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include warnings, request log identifiers, replacement counts, or asynchronous task identifiers for large document updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

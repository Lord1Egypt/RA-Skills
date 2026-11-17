## Description:

Word文档 (.docx) 处理，支持修订模式(Track Changes)和批注操作。使用场景：(1) 修订模式 - 添加插入/删除修订、红字标注；(2) 批注操作 - 添加、删除、查看批注；(3) 文档内容修改。当用户要求"修订"、"track changes"、"批注"、"红字修订"、"添加评论"、"添加注释"时触发此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanselxie](https://clawhub.ai/user/hanselxie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to modify Word DOCX documents by enabling track changes, adding insertion or deletion revisions, and working with comments through OOXML-oriented guidance and helper commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Revision and comment behavior may alter documents unexpectedly or give users an inaccurate impression of legally reliable Word comments or auditable Track Changes.

Mitigation: Review generated DOCX files manually in Word-compatible software before relying on comments, revisions, or audit trails.

Risk: The documented fixed temporary-directory workflow can overwrite or mix files when reused across documents.

Mitigation: Use a fresh temporary directory per document and verify archive contents before repacking the DOCX.

Risk: The helper script's comment path may insert visible inline text rather than a real Word comment.

Mitigation: Treat script-added comment text as visible document content unless the final DOCX is inspected and confirmed to contain proper Word comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanselxie/skills/docx-trackchanges-and-comments)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline XML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and commands for editing DOCX files; output documents should be manually checked in Word-compatible software.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

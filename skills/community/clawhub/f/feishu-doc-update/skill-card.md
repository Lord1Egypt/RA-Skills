## Description:

更新飞书云文档，支持追加、覆盖、定位替换、全文替换、前后插入和删除等 7 种更新模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent update existing Feishu cloud documents by appending, replacing, inserting, deleting, or retitling content with precise selectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive modes such as overwrite, delete_range, replace_all, or empty-content replacements can remove document content or hard-to-rebuild embedded material.

Mitigation: Verify the doc_id and selector carefully, prefer narrow unique selections, and use preview or explicit confirmation before applying destructive edits.

Risk: Broad or ambiguous selectors can modify the wrong section or multiple unintended matches.

Mitigation: Use precise text ranges or title-based selections and keep replacement scopes as small as possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/skills/feishu-doc-update)

## Skill Output:

**Output Type(s):** [JSON, Markdown, API Calls, Guidance]

**Output Format:** [JSON responses and Markdown document content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return success details, warnings, log_id, asynchronous task_id status, or structured error messages.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

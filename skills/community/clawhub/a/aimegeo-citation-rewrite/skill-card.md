## Description:

根据用户问题和可信资料优化现有文章的 AI 引用可读性，在授权范围内改稿，并检查保留段落与证据记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要修订现有文章的用户。根据用户指定的问题、来源和可编辑章节，调整文章并交付完整稿、变更说明及待核实事项。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Revisions could change sections the user did not authorize or lose the original wording.

Mitigation: Confirm editable sections first, preserve the original article, and review the change note; use the local checker for supported scope checks.

Risk: A passing structural check does not establish that factual claims or citations are accurate.

Mitigation: Review each claim against its source and independently check factual accuracy; treat unsupported claims as unresolved or remove them.

Risk: Using aimeGeo may involve uploading article content or publishing it through connected accounts.

Mitigation: Decide separately whether to upload content or publish, and review the article before sharing it.

## Reference(s):

- [检查计划格式](references/check-format.md)
- [aimeGeo AI 引用文档](https://geo.aimmme.com/docs/ai-citations/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, JSON]

**Output Format:** [Markdown article revision with a change note and unresolved-facts list; optionally a JSON check plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [An optional local checker evaluates limited structure and scope rules; it does not establish factual accuracy or citation outcomes.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

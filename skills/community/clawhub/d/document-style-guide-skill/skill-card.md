## Description:

中文技术文档写作规范助手，帮助用户撰写、审校、润色或重写中文技术文档，包括 README、API 文档、产品手册、博客、教程、changelog 和 UI 文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares0x](https://clawhub.ai/user/ares0x)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, developers, and product teams use this skill to review, rewrite, and generate Chinese technical documentation and UI copy against an opinionated style guide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies an opinionated Chinese technical writing style and may over-apply those conventions to bilingual, non-Chinese, or project-specific style requirements.

Mitigation: State the target language, bilingual expectations, and project style exceptions before asking the agent to review or rewrite content.

Risk: Rewrite mode may change tone, wording, or structure in ways that alter the author's intended meaning.

Mitigation: Review rewritten documents before publication, especially examples, product claims, numbers, and user-facing UI messages.

## Reference(s):

- [Server-resolved source repository](https://github.com/ares0x/document-style-guide-skill)
- [ClawHub skill page](https://clawhub.ai/ares0x/skills/document-style-guide-skill)
- [Reference: title rules](references/title.md)
- [Reference: text rules](references/text.md)
- [Reference: paragraph rules](references/paragraph.md)
- [Reference: number rules](references/number.md)
- [Reference: punctuation rules](references/marks.md)
- [Reference: document structure](references/structure.md)
- [Reference: Markdown rules](references/markdown.md)
- [Reference: terminology rules](references/terminology.md)
- [Reference: UI copy rules](references/ui-copy.md)
- [Reference: changelog rules](references/changelog.md)
- [Reference: review checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, tables, rewritten documents, and short change summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review mode returns issue summaries and suggested edits; rewrite mode returns revised Chinese documentation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

智能电子书阅读助手，支持EPUB/PDF等常见格式解析；提供章节总结、关键内容摘录、深度分析与落地应用建议；当用户需要阅读电子书、做读书笔记或寻求知识转化方案时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to parse EPUB/PDF ebooks and produce chapter-by-chapter notes, excerpts, analysis, application advice, full-book synthesis, and further-reading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes the full contents of user-provided ebooks or PDFs, which may include confidential, private, or copyrighted text.

Mitigation: Use the skill only with files the user is authorized to process, and avoid sensitive documents unless the environment and retention policy are appropriate.

Risk: Generic reading-note prompts may trigger the skill even when the user did not intend ebook processing.

Mitigation: Confirm that the task involves an EPUB/PDF ebook before invoking the parser or analyzing uploaded file contents.

Risk: PDF parsing may lose formatting, and scanned PDFs may require OCR before useful text can be extracted.

Mitigation: Prefer EPUB or text-based PDF inputs, and run OCR first for scanned PDFs before relying on summaries or analysis.

## Reference(s):

- [Reading Framework](references/reading-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/ludiansheng/skills/ebook-reader)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reading notes and structured JSON parser output, with shell commands for ebook parsing when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [EPUB/PDF input is parsed into structured chapter data before the agent writes summaries, excerpts, analyses, and recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence, claw.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

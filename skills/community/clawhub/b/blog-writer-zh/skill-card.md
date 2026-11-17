## Description:

Writes Chinese long-form technology commentary, industry analysis, and personal reflective essays with a critical, structured style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavier-ljf](https://clawhub.ai/user/xavier-ljf)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, creators, and analysts use this skill to draft, revise, review, humanize, export, and archive Chinese long-form articles for technology commentary, industry analysis, and platforms such as WeChat, Zhihu, and Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read recent Markdown files from BLOG_REFERENCES_DIR to calibrate writing style.

Mitigation: Set BLOG_REFERENCES_DIR to a narrow reference-only directory and keep sensitive or unrelated documents outside that path.

Risk: The workflow writes local drafts and export files, and its archive step may clean generated export files.

Mitigation: Review output paths and generated files before export cleanup or final archiving.

Risk: The writing workflow may use web research to support claims on current or sensitive topics.

Mitigation: Review cited sources and approve research scope before relying on factual claims.

## Reference(s):

- [Skill page](https://clawhub.ai/xavier-ljf/skills/blog-writer-zh)
- [Writing Style Guide](references/style-guide.md)
- [Article Structure Templates](references/templates.md)
- [Pandoc](https://pandoc.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown drafts and export files with concise agent guidance and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local draft Markdown files, platform-compatible Markdown exports, and optional DOCX exports when pandoc is installed.]

## Skill Version(s):

1.1.0 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

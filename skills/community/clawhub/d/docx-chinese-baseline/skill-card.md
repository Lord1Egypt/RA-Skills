## Description:

Provides a locked visual baseline and conversion workflow for Chinese Word/DOCX documents and WeChat-native articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and developers use this skill to produce consistent Chinese DOCX or WeChat article layouts and recover when HTML-to-DOCX conversion loses styles or fails on Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is partial; it notes an unresolved local reference and a low-probability self-modification alert.

Mitigation: Review the skill and resolve the missing reference before relying on its guidance.

Risk: HTML-to-DOCX conversion can lose styles or render Chinese glyphs incorrectly on some systems.

Mitigation: Reopen the DOCX and verify sizes, heading color, CJK glyphs, editability, and layout; use the documented recovery path when conversion fails.

## Reference(s):

- [Chinese DOCX Typesetting Baseline on ClawHub](https://clawhub.ai/haiyangchenbj/skills/docx-chinese-baseline)

## Skill Output:

**Output Type(s):** [DOCX files, Markdown reports, Formatting guidance]

**Output Format:** [Editable DOCX document with a concise Markdown verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed typography tokens and explicit layout and spacing rules.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

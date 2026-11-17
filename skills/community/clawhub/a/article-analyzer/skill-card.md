## Description:

Analyzes WeChat or web articles when asked to break down, study, or learn from an article, covering structure, memorable lines, topic logic, emotional arc, and reusable writing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, marketers, and writing-focused agents use this skill to analyze article structure, headline techniques, memorable sentences, audience fit, emotional progression, and reusable writing patterns from user-provided article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated analysis may be based on incomplete or incorrect fetched article content.

Mitigation: Review the retrieved article text and source metadata before relying on the report.

Risk: When a user requests Feishu document creation, the generated report is sent to Feishu.

Mitigation: Use chat output instead for content that should not be placed in Feishu.

## Reference(s):

- [Article headline and structure patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report, with optional Feishu document creation when the user requests it]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is chat text; quick mode returns a shorter four-part analysis.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-04-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

内容改写与风格模仿。当用户要求将文本改写成不同语气/风格时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyiz51](https://clawhub.ai/user/wuyiz51)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing-focused agents use this skill to rewrite Chinese text into requested tones or named writing styles while preserving the original core information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as organizing files or categorizing summaries may activate the skill for unrelated writing tasks.

Mitigation: Confirm the user wants style rewriting when the request is ambiguous before applying the skill workflow.

Risk: Named-style rewriting can change tone and presentation enough to reduce information density or distort emphasis.

Mitigation: Preserve core facts and call out major changes after the rewrite, as the artifact's workflow requires.

## Reference(s):

- [Writing Styles Reference](references/writing-styles.md)
- [ClawHub skill page](https://clawhub.ai/wuyiz51/skills/content-style-rewriter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with rewritten text, style summary, and change notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to choose a target style when none is specified.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

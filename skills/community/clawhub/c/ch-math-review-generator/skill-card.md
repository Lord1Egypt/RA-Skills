## Description:

Generates junior-high math review guide HTML files with knowledge summaries, embedded SVG diagrams, practice questions, answers, and validation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangmange](https://clawhub.ai/user/wangmange)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, students, parents, and tutoring agents use this skill to create Chinese junior-high math review materials for chapter study, exam preparation, practice sets, and mistake review. The generated materials combine concept summaries, SVG diagrams, exercises, and step-by-step explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create HTML files automatically in the current working directory.

Mitigation: Use it in a dedicated workspace or review the output path before accepting generated files.

Risk: The skill requires persistent task logging under .workbuddy/memory.

Mitigation: Review or disable memory logging where persistent records are not desired.

Risk: The broad activation wording may cause ordinary math help requests to generate files unexpectedly.

Mitigation: Confirm the user's intent to create a full review document before running the generation workflow.

## Reference(s):

- [HTML Template and Validation Guide](artifact/references/template_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/wangmange/skills/ch-math-review-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML files with embedded SVG, plus Markdown-style guidance and shell commands for validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates files in the working directory and may append task records under .workbuddy/memory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

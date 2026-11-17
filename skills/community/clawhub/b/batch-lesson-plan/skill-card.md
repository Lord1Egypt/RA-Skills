## Description:

Turns a teaching schedule and textbook material into a batch of Chinese-language secondary vocational lesson plans in DOCX format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yon-gjun](https://clawhub.ai/user/yon-gjun)

### License/Terms of Use:

Apache License 2.0

## Use Case:

Teachers and educational staff use this skill to turn a course teaching schedule and scanned textbook pages into a set of editable secondary vocational lesson plans, with optional supporting classroom materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated teaching content may be inaccurate or incomplete when source PDFs or templates are unsuitable.

Mitigation: Use trusted templates and PDFs, confirm the lesson list before batch generation, and review each generated plan for accuracy.

Risk: An existing file at the specified output path may be overwritten.

Mitigation: Choose a new output path or back up any existing file before running the helper.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yon-gjun/skills/batch-lesson-plan)
- [Server-resolved source repository](https://github.com/yon-gjun/batch-lesson-plan)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [DOCX lesson plans, intermediate JSON content, and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks generated DOCX table structure; requires a suitable lesson-plan template and user-reviewed source material.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

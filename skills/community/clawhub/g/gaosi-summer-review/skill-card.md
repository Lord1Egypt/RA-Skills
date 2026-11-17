## Description:

Builds structured summer review plans and quantifiable check-in sheets for grades 4-6 using the Gaosi Guide competition-math knowledge tree, with tiered topic coverage and PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuolongbj](https://clawhub.ai/user/shuolongbj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, parents, tutors, and education-support agents use this skill to assemble Gaosi Guide summer review schedules, daily check-in tables, and printable study-plan deliverables for elementary competition-math review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF export launches a local Chrome, Edge, or Chromium process and writes generated HTML/PDF files.

Mitigation: Review the input HTML and output paths before export, and use the export command only for intended study-plan files.

Risk: The skill may suggest a local static server for previewing generated files.

Mitigation: Bind preview servers to 127.0.0.1 and stop them after reviewing the generated plan.

## Reference(s):

- [高思导引知识树](references/knowledge-tree.md)
- [高思导引暑假总复习工作流](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/shuolongbj/skills/gaosi-summer-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language study plans, check-in tables, HTML templates, PDF export commands, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or copy HTML/PDF files, launch a local Chromium-family browser for PDF export, and optionally use a localhost-only static server for previewing generated files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

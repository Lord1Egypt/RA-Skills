## Description:

Local homework-grading scripts score JSON submissions against answer keys, apply simple rubric-based partial credit for subjective answers, and render student or teacher feedback reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, tutors, and learners can use this skill to score homework submissions, review per-item feedback, and generate reports for instructional follow-up. Use it as a local grading aid with human review, especially for subjective answers or high-stakes grades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised OCR, photo/PDF parsing, batch reports, and advanced error-analysis features are not evidenced in the current scripts.

Mitigation: Use the included JSON-based grading pipeline unless those additional capabilities are independently verified in a later release.

Risk: Homework submissions and generated reports may contain student personal information.

Mitigation: Avoid unnecessary student PII in input and output files, and keep generated reports in appropriate local storage.

Risk: Automated scoring can be incorrect or incomplete, especially for subjective answers.

Mitigation: Require teacher review before using results for transcripts, formal grades, or other high-stakes decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/boboy-j/skills/edu-homework-grader)
- [Project homepage](https://github.com/openclaw-skills/edu-homework-grader)
- [Curriculum reference example](knowledge/curriculum_rpep.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON grading results and Markdown-style student or teacher reports, with example shell commands for local execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs against local JSON homework and answer-key files; reports should be reviewed by a teacher before high-stakes use.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

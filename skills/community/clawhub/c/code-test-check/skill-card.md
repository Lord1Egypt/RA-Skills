## Description:

Analyzes user-provided PRD documents or functional test cases against specified backend and frontend source code, then produces a Markdown implementation verification report with code evidence and status matrices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxpfreesky](https://clawhub.ai/user/zxpfreesky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and project reviewers use this skill to statically verify whether requirements or functional test cases are implemented in selected frontend and backend code, with evidence-backed findings and regression-impact analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report can include code paths, code snippets, and analysis of sensitive repositories or requirements documents.

Mitigation: Run the skill only on intended PRD/test files and narrowly scoped source directories, and confirm the report output path before use.

## Reference(s):

- [Tech Stack Guide](references/tech-stack-guide.md)
- [Report Template](report/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables, code evidence, implementation status, risk notes, and regression-impact guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content depends on the user-provided PRD or test cases and the source directories selected for static analysis.]

## Skill Version(s):

1.5.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

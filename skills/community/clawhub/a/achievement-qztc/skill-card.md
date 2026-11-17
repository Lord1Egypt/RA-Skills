## Description:

Generates and reviews QZTC course objective achievement analysis reports from local grade spreadsheets, with pipeline generation, review checks, and template-derived weights and target configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alukardo](https://clawhub.ai/user/alukardo)

### License/Terms of Use:

MIT-0

## Use Case:

QZTC internal course staff and supporting agents use this skill to generate course objective achievement analysis DOCX reports from Excel grade data and to review the generated reports for placeholder replacement, tables, charts, and analysis paragraphs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can contain student grade data.

Mitigation: Run the skill only on intended local course folders and protect generated DOCX reports according to the institution's student-data handling rules.

Risk: Report edits and template copying affect local course files.

Mitigation: Use copies of source spreadsheets and templates when testing or reviewing a new release.

Risk: Generated analysis text may include a course-specific data visualization conclusion.

Mitigation: Review the final report for course fit and accuracy before sharing or archiving it.

## Reference(s):

- [Course Objective Achievement Formula](references/grading-formula.md)
- [ClawHub Skill Page](https://clawhub.ai/alukardo/skills/achievement-qztc)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Analysis, Configuration instructions]

**Output Format:** [DOCX reports with terminal and optional JSON review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local Excel spreadsheets and Word templates; generated reports can contain student data.]

## Skill Version(s):

5.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

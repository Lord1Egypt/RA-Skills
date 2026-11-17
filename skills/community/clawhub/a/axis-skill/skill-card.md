## Description:

Axis is a Chinese Gaokao admissions advisor that helps evaluate majors, universities, application strategy, and AI-era employability risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares0x](https://clawhub.ai/user/ares0x)

### License/Terms of Use:

MIT-0

## Use Case:

Students, families, and education advisors use Axis to collect applicant profile information, evaluate Holland-interest and employability factors, and generate Chinese Gaokao major and university application guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad shell execution and includes unsafe patterns that place student-supplied values into command strings.

Mitigation: Review before installing and change the shell workflow to pass user values safely instead of interpolating them into commands.

Risk: Student profile details, assessment answers, snapshots, and generated reports may be stored locally.

Mitigation: Use it only in an appropriate workspace and manage access, retention, and deletion of locally stored student data.

Risk: The package may be incomplete if referenced scripts and data files are absent.

Mitigation: Confirm the release includes the referenced scripts and data before relying on its admissions guidance or reports.

## Reference(s):

- [Source repository](https://github.com/ares0x/axis-skill)
- [ClawHub skill page](https://clawhub.ai/ares0x/skills/axis-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown conversational guidance with optional inline shell commands and saved report paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store local student profile details, assessment answers, snapshots, and reports when its workflow is used.]

## Skill Version(s):

2.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

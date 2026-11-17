## Description:

Generates a customizable, data-driven single-page exam practice site with daily question selection, answer checking, a mistake book, weekly analysis, and question bank management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzjmay123](https://clawhub.ai/user/zzjmay123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and educators use this skill to scaffold a static exam-practice site for standardized exams by creating a JSON question bank, customizing the HTML template, and configuring daily question rotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted question-bank or saved wrong-answer content can create stored browser XSS in the shipped web template.

Mitigation: Render question data with textContent or sanitized HTML, remove inline event handlers, validate JSON fields, and treat localStorage as untrusted before using imported, shared, or user-contributed question banks.

Risk: The optional cron or launchd updater may run an unintended path or schedule if enabled without review.

Mitigation: Only enable scheduled updates after confirming the updater path and schedule are exactly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzjmay123/skills/exam-practice-site)
- [Skill README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, HTML, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a static single-page site scaffold and local JSON data files; generated question content must be supplied or verified by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

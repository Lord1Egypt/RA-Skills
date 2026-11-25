## Description:

This skill turns a teaching schedule into a batch of vocational lesson plans in Word (.docx).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yon-gjun](https://clawhub.ai/user/yon-gjun)

### License/Terms of Use:

Apache 2.0

## Use Case:

Vocational teachers use it to turn a teaching schedule and textbook material into printable lesson plans. They review the extracted lesson list and hour assignments before batch generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security guidance says the scan was partial, some local path references did not resolve, and runtime permissions were not verified.

Mitigation: Review the unresolved references and grant only the access needed before using the skill.

## Reference(s):

- [Server-resolved source repository](https://github.com/yon-gjun/batch-lesson-plan)
- [ClawHub skill release](https://clawhub.ai/yon-gjun/skills/batch-lesson-plan)
- [WorkBuddy conversation archive](https://workbuddy.cn)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Printable Microsoft Word (.docx) lesson plans; lesson content is organized as structured JSON during generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate one document per confirmed lesson topic and reports whether the resulting document structure passes validation.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

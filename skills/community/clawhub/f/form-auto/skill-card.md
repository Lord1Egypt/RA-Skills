## Description:

Form Auto helps OpenClaw agents fill web forms automatically for job applications, registrations, surveys, and other standard HTML forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill to detect web form fields, map them to user-provided profile data, fill the form, and present the filled values for review before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive form values may appear in console or agent output while an authenticated browser session is used.

Mitigation: Use the skill only on trusted sites, avoid forms containing credentials, payment data, tokens, or hidden sensitive fields, and review output carefully.

Risk: The skill can enter user data into third-party websites on the user's behalf.

Mitigation: Keep the review-before-submit step, confirm filled values with the user, and do not submit forms automatically without explicit confirmation.

Risk: Saved templates may retain sensitive identity data.

Mitigation: Avoid storing highly sensitive profile data unless the storage location and deletion process are understood.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/form-auto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw v2026.3.22+ with browser access; filled forms should be reviewed before submission.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

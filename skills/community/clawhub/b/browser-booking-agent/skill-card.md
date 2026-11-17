## Description:

Execute booking/search flows via browser automation with verification artifacts for reservation forms, availability checks, and proof capture such as screenshots and confirmation IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austineyapp](https://clawhub.ai/user/austineyapp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to complete browser-based booking or search workflows, capture verification evidence, and return a concise completed, blocked, or needs-user-input status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent could reach a payment or final submission step during a booking flow.

Mitigation: Require explicit user approval before payment or final submission, and have the user verify the final details before proceeding.

Risk: The booking workflow may encounter login, captcha, or 2FA controls.

Mitigation: Stop at login, captcha, or 2FA prompts and request user action instead of attempting to bypass access controls.

Risk: Incorrect booking details could be entered or submitted.

Mitigation: Collect only the task details needed, preserve verification evidence, and report key parameters, prices, cancellation terms, confirmation IDs, and screenshot paths.

## Reference(s):

- [Verification Checklist](references/verification-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/austineyapp/skills/browser-booking-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise Markdown status with verification details and screenshot paths when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include completed, blocked, or needs-user-input status; confirmation IDs; prices; cancellation terms; and evidence paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Register Cliento booking pages via URL, check availability, and execute actual service bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to register trusted Cliento booking pages, check appointment availability, temporarily reserve slots, and confirm service bookings after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration helper can fetch arbitrary URLs and print raw page contents.

Mitigation: Use the skill only with trusted Cliento booking URLs and review fetched content before acting on it.

Risk: Booking confirmation sends contact details, optional notes, and possibly a PIN to Cliento APIs.

Mitigation: Confirm every live booking step with the user and collect only the details needed to complete the booking.

Risk: Saved contact details in USER.md may be reused in later bookings.

Mitigation: Save contact details only after explicit user approval and avoid persistence when reuse is not intended.

## Reference(s):

- [Cliento Booker on ClawHub](https://clawhub.ai/patello/skills/cliento-booker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update ./.cliento/stores.json and USER.md when the user explicitly provides or approves saved booking details.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Manage Booking.com properties by downloading reservations, listing or replying to guest messages, and updating rates through a Python CLI that automates the Booking.com extranet in local Chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matsei-ruka](https://clawhub.ai/user/matsei-ruka)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers and hospitality operators use this skill to have an agent run local Booking.com extranet workflows such as reservation export, guest-message review and replies, and rate updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unpinned external code that handles Booking.com credentials and persistent browser sessions.

Mitigation: Use a pinned, audited commit of the external repository, lock and verify dependencies, and protect the .env and .chrome-data files.

Risk: Guest messages and rate changes affect live Booking.com accounts.

Mitigation: Require explicit human approval with a preview before sending guest messages or changing rates.

Risk: Local Chrome automation and persisted browser session data can expose account access if the host is not protected.

Mitigation: Keep Chrome remote debugging bound to localhost, restrict access to the bot directory, and delete persisted session data when access should be revoked.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/matsei-ruka/skills/booking-extranet-manager)
- [External CLI dependency referenced by the skill](https://github.com/matsei-ruka/booking-extranet-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce JSON on stdout or Excel files through the external CLI.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

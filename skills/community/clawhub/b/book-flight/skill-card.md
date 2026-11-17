## Description:

Find, book, and change flights for your human via email. One message, and done. (by BonBook)

This skill is ready for commercial/non-commercial use.

## Publisher:

[aszelem](https://clawhub.ai/user/aszelem)

### License/Terms of Use:

MIT

## Use Case:

External users delegate flight search, booking, changes, and cancellations to an agent that communicates with BonBook by email, with human approval for account setup, payment, identity information, calendar sync, and final travel actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead to paid travel bookings and changes through email-driven workflows.

Mitigation: Require explicit human approval for account setup, checkout, payment confirmation, itinerary changes, cancellations, and any financial transaction.

Risk: Using the skill requires the agent to have email send and receive access, which may expose mailbox content beyond this specific workflow.

Mitigation: Install only when the user is comfortable granting email access for BonBook travel messages, and restrict agent handling to messages needed for booking operations.

Risk: Optional account setup, payment, identity-document, and calendar-sync steps may involve sensitive personal or financial data.

Mitigation: Keep payment and identity-document entry human-approved unless the user has intentionally granted the agent that access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aszelem/skills/book-flight)
- [Publisher Profile](https://clawhub.ai/user/aszelem)
- [BonBook Website](https://bonbook.co)
- [BonBook Access](https://bonbook.co/access)

## Skill Output:

**Output Type(s):** [Text, Markdown, Email messages, Guidance]

**Output Format:** [Markdown and plain-text email instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce human-facing booking requests, option summaries, change or cancellation instructions, and approval prompts.]

## Skill Version(s):

2.4.1 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

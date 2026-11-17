## Description:

Customer Visit Prep helps sales users prepare for customer meetings by turning a customer name, background, and visit goal into a customer brief, visit strategy, talk tracks, objections, and preparation checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and account managers use this skill to prepare customer visits with customer-specific research, MEDDIC-based discovery questions, FABE value framing, usable talk tracks, anticipated objections, and materials to bring to the meeting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent customer memory may contain sensitive business or account information without clear confirmation or retention controls.

Mitigation: Require user confirmation before reading or writing customer memory, preview saved content, and apply retention controls appropriate for customer and sales data.

Risk: Customer names may be used in memory paths.

Mitigation: Constrain and sanitize customer-name paths before accessing or appending customer memory files.

Risk: Generated visit documents may be sent through enterprise messaging to unintended recipients.

Mitigation: Confirm recipients and content before sending generated documents through enterprise messaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/skills/customer-visit-prep)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown text in chat, with optional Markdown or Word documents when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include customer research summaries, visit strategy tables, talk tracks, objection handling, and preparation material lists.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

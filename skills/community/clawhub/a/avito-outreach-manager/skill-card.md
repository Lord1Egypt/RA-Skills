## Description:

Review Avito message drafts for clarity, consent, respectful tone, one clear next step, and safe checkout wording before a human decides what to send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to review seller-facing Avito message drafts for respectful wording, one clear next step, and payment-safe language before deciding what to send.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste sensitive personal, payment, cookie, or full private-chat data into a message-review prompt.

Mitigation: Only provide the context needed for copy review and omit sensitive identifiers, payment details, session data, and private chat exports.

Risk: Draft-review output could be mistaken for account activity or payment instructions.

Mitigation: Use the skill only for draft QA; keep Avito account actions and payment decisions outside the skill and manually decide what to send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/avito-outreach-manager)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing a revised message, change summary, human-send checklist, and payment-safety reminder]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

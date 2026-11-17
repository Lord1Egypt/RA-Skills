## Description:

Analyzes email inbox health with weather metaphors, spam/signal classification, email debt scoring, ghost detection, and time-cost estimates using the himalaya CLI over configured IMAP email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to assess inbox status, email backlog, signal versus noise, and people waiting for replies from a configured IMAP mailbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can expose sender names, subject lines, contacts, and communication patterns from configured email accounts.

Mitigation: Run the skill only intentionally for mailbox analysis and treat text or JSON outputs as sensitive.

Risk: The skill reads email metadata from the configured email account through himalaya.

Mitigation: Install only when comfortable granting local mailbox metadata access and avoid automatic routing of casual email questions to this skill.

## Reference(s):

- [Email Intelligence on ClawHub](https://clawhub.ai/pfrederiksen/skills/email-intelligence)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain-text report or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sender names, subject lines, contacts, and communication patterns from the configured email account.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

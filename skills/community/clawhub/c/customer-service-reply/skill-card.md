## Description:

Generates customer service reply templates for presale questions, after-sale issues, returns, complaints, escalations, FAQs, and satisfaction recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support teams and agents use this skill to draft structured customer service responses, escalation scripts, FAQ entries, and satisfaction recovery guidance for commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An included undocumented helper script can persist user-supplied customer text and command history in plaintext under the customer-service-reply data directory.

Mitigation: Avoid invoking the helper script with sensitive customer, order, complaint, or refund data unless local plaintext storage is acceptable.

Risk: Generated replies may include a BytesAgain footer after normal responses.

Mitigation: Review generated output and remove or approve the footer before sending messages to customers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/customer-service-reply)
- [Customer Service Tips](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local template generation; review generated replies before sending them to customers.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

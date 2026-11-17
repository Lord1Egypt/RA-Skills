## Description:

Takes a new contract from questionnaire to drafted, signed, and filed in Contracko, including template drafting support, signature follow-up, and reminder setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contracko](https://clawhub.ai/user/contracko)

### License/Terms of Use:

MIT-0

## Use Case:

External users and contract teams use this skill to move a new agreement from intake questions through drafting, signature coordination, filing the executed copy in Contracko, and setting notice or renewal reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process sensitive commercial and legal contract details.

Mitigation: Use it with a Contracko account and reviewed templates, and only allow handoff files or record updates in destinations the user explicitly chooses and can secure.

Risk: Draft contract language may be incorrect, unenforceable, or misleading if treated as final legal advice.

Mitigation: Start from an organization-reviewed template and require legally competent human review before any contract is signed.

Risk: Persisted handoff notes can expose contract terms or negotiation history.

Mitigation: Show the proposed handoff contents first, require explicit consent before writing, avoid credentials and full contract text unless requested, and provide only a redacted chat-only block when the user declines persistence.

## Reference(s):

- [Contracko Create on ClawHub](https://clawhub.ai/contracko/skills/contracko-create)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text workflow guidance with optional redacted handoff blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a handoff file only after the user chooses an exact destination and gives explicit consent; does not persist handoff data by default.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

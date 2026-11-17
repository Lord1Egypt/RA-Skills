## Description:

Agent assistant pour entrepreneurs et freelances francophones qui gere les emails professionnels, genere des devis et factures, relance les clients, prepare des briefs, automatise la prospection et parle francais nativement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yerrochdi](https://clawhub.ai/user/yerrochdi)

### License/Terms of Use:

MIT

## Use Case:

External entrepreneurs and freelancers serving French-speaking clients use this skill to draft professional emails, prepare quotes and invoices, write payment reminders, brief client meetings, and create prospecting messages. The skill is draft-only and expects user review before any message or document is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive business identity, banking, or client details may be placed in broad agent memory.

Mitigation: Keep shared USER.md or MEMORY.md entries limited to non-sensitive defaults, provide IBANs, tax IDs, addresses, and client details only when needed for a specific document, and remove them when no longer required.

Risk: Generated business documents or legal mentions may not match the user's exact commercial, tax, or client situation.

Mitigation: Review invoices, quotes, reminders, payment terms, TVA details, SIRET information, and late-payment clauses before sending or sharing them externally.

## Reference(s):

- [French Business Assistant homepage](https://github.com/yerrochdi/french-business-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown or plain text, with optional simple HTML for quote and invoice drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only business communications and documents intended for user review before external use]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

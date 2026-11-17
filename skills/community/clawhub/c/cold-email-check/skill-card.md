## Description:

Checks if a cold email to a specific address is legal before you send it (UK, US, Canada, Germany, France, Australia, Ireland, Netherlands), with a receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabrielaoimevbore-beep](https://clawhub.ai/user/gabrielaoimevbore-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers can check whether a proposed cold email to a specific address is appropriate before sending it, based on the sender's country, outreach facts, and recipient details. They use the result to guide next steps and include any required email footer; the skill does not send email.

### Deployment Geography for Use:

Sender businesses based in the UK, US, or UAE; full recipient rules for the UK, US, Canada, Germany, France, Australia, Ireland, and the Netherlands, with limited responses elsewhere.

## Known Risks and Mitigations:

Risk: Recipient addresses and outreach facts are sent to Precleared, whose privacy and retention terms could not be independently verified.

Mitigation: Review Precleared's privacy and retention terms, and use --dry-run to preview submissions before sending data.

Risk: Receipt links may expose check details to anyone who has the link.

Mitigation: Protect receipt links and share them only with authorized people.

Risk: Eligibility results could be mistaken for a legal guarantee.

Mitigation: Treat the result as decision support rather than legal advice or a guarantee.

## Reference(s):

- [Precleared homepage](https://precleared.dev)
- [Precleared rules](https://precleared.dev/rules)
- [Precleared API documentation](https://precleared.dev/docs)
- [ClawHub skill page](https://clawhub.ai/gabrielaoimevbore-beep/skills/cold-email-check)

## Skill Output:

**Output Type(s):** [Guidance, Structured data]

**Output Format:** [Concise text with an eligibility verdict and receipt details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision support includes the deciding rule and source, footer requirements, and next steps; it does not send email.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

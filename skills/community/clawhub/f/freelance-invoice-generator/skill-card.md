## Description:

Generate professional, client-ready freelance invoices in Markdown or HTML from a simple JSON job file with line items, tax rate, discounts, and late-fee terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, consultants, and developers use this skill to generate client-ready Markdown or HTML invoices from a JSON job file, including line items, subtotal, discount, tax, due-date, and late-fee language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML invoice output can include unescaped invoice data from untrusted JSON.

Mitigation: Use trusted local job files, prefer Markdown output for lower-risk workflows, and escape invoice fields before generating or sending HTML invoices from client-supplied, downloaded, or shared JSON.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/skills/freelance-invoice-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets; the bundled script produces Markdown or HTML invoice files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standard-library Python script; no external API, account, or subscription required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

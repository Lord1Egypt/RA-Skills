## Description:

Generate professional invoices for ClawHub/OpenClaw skill development services, including standard rates, Saskatchewan GST calculations, multi-item billing, and HTML/PDF-oriented invoice output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunnyo](https://clawhub.ai/user/skunnyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and independent ClawHub/OpenClaw skill builders use this skill to prepare client invoices, quotes, and monthly billing summaries for custom AgentSkill work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client invoice data can contain sensitive business and contact information.

Mitigation: Treat invoice JSON and generated invoices as sensitive, avoid untrusted input, and review files before sharing.

Risk: Invoice fields are rendered into HTML/PDF-oriented output, which can carry malformed or unsafe content if inputs are not controlled.

Mitigation: Escape or sanitize invoice fields before generating distributable HTML or PDF files.

Risk: Release security evidence notes quality and local-file safety issues in the invoice generator script.

Mitigation: Review or fix the script before use and run it only with trusted local JSON files.

## Reference(s):

- [Saskatchewan Tax & ClawHub Dev Invoice Guidelines](references/sask_tax_guidelines.md)
- [ClawHub skill release page](https://clawhub.ai/skunnyo/skills/clawhub-dev-invoice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and generated HTML invoice files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated invoices use CAD amounts and calculate 5% GST from subtotal plus expenses.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

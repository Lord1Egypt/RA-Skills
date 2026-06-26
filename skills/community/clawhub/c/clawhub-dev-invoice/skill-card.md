## Description: <br>
Generate professional invoices for ClawHub/OpenClaw skill development services, including custom AgentSkill creation, editing, testing, publishing, standard rates, Saskatchewan GST calculation, multi-item support, and PDF/HTML output via bundled templates and scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skunnyo](https://clawhub.ai/user/skunnyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and freelance ClawHub/OpenClaw skill builders use this skill to prepare invoices or quotes for custom skill development, publishing, testing, debugging, expenses, and rush work. It supports local invoice data collection, CAD line-item calculation, Saskatchewan GST handling, and HTML/PDF invoice generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoices and sample inputs can contain client names, addresses, emails, amounts, and payment details. <br>
Mitigation: Keep invoice JSON, HTML, and PDF outputs out of repositories and share them only through appropriate billing channels. <br>
Risk: Tax, sender, client, and payment details may be incorrect for a specific invoice. <br>
Mitigation: Review client data, payment instructions, line items, CAD amounts, and Saskatchewan GST assumptions before sending an invoice. <br>
Risk: The bundled Python and JSON appear HTML-escaped and may need correction before execution. <br>
Mitigation: Validate the script and generated invoice locally before relying on it for billing. <br>


## Reference(s): <br>
- [Saskatchewan Tax and ClawHub Dev Invoice Guidelines](references/sask_tax_guidelines.md) <br>
- [ClawHub skill page](https://clawhub.ai/skunnyo/clawhub-dev-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON invoice inputs, shell commands, and generated HTML/PDF invoice artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local workflow; invoice JSON, HTML, and PDF outputs may contain client billing details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

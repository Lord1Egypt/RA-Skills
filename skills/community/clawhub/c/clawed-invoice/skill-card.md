## Description: <br>
Generate professional PDF invoices with a clean layout, no browser dependency, and support for EUR, GBP, USD, multi-item tables, custom brand colours, and payment details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexwong27](https://clawhub.ai/user/alexwong27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to generate branded invoice PDFs from structured invoice JSON and local company configuration in constrained Node.js environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated invoice PDFs may contain customer addresses, account references, IBAN/SWIFT details, or other sensitive business data saved to disk. <br>
Mitigation: Use a private output directory, protect or delete generated PDFs according to retention needs, and avoid shared temporary locations for sensitive invoices. <br>


## Reference(s): <br>
- [Clawed Invoice Generator on ClawHub](https://clawhub.ai/alexwong27/clawed-invoice) <br>
- [Default invoice configuration](references/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration] <br>
**Output Format:** [PDF file written to a local output directory, with shell-command usage and JSON configuration inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output path is /tmp/invoices; invoice filenames are derived from the invoice number.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

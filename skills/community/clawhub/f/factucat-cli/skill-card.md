## Description:

Use this skill when an agent needs to install, update, authenticate, or operate the FactuCat CLI to create Mexican CFDI 4.0 invoice drafts, assign customers or receiver data, add concepts, preview invoices, stamp them, send them through customer contact channels, or download XML/PDF artifacts on factucat.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ocruzv](https://clawhub.ai/user/ocruzv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to install, authenticate, and run FactuCat CLI workflows for Mexican CFDI 4.0 invoice drafts, previews, stamping, customer delivery, and XML/PDF artifact downloads.

### Deployment Geography for Use:

Mexico, for Mexican CFDI 4.0 invoicing workflows.

## Known Risks and Mitigations:

Risk: Unattended stamping or customer-delivery commands can issue or send fiscally significant invoices.

Mitigation: Require a deliberate human review of the full invoice preview before unattended stamp or customer-send commands.

Risk: Live FactuCat API keys may be exposed if pasted into shell commands, prompts, logs, or shell history.

Mitigation: Avoid placing live keys in command text; use interactive entry, standard input, or managed secrets where available.

Risk: An unpinned global npm install may install a CLI version that has not been reviewed for the release.

Mitigation: Prefer an explicit reviewed @factucat/cli version and confirm trust in the npm package and publisher before installation.

## Reference(s):

- [FactuCat CLI source](https://github.com/factucat/ai-skills/tree/main/factucat-cli)
- [FactuCat production service](https://factucat.com)
- [Install and authenticate](references/install-and-auth.md)
- [Interactive flows](references/interactive-flows.md)
- [Unattended flows](references/unattended-flows.md)
- [Mexican CFDI 4.0 context](references/mexico-cfdi-context.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FactuCat CLI commands that create, preview, stamp, send, or download CFDI invoice artifacts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

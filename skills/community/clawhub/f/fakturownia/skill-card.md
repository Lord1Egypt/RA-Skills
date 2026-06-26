## Description: <br>
Fakturownia CLI helps agents authenticate, discover schemas, run diagnostics, and operate major Fakturownia API areas through the `fakturownia` command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sixers](https://clawhub.ai/user/sixers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide an agent through Fakturownia CLI setup and billing workflows, including accounts, clients, invoices, payments, warehouse records, webhooks, KSeF flows, and recurring invoices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may create, update, delete, email, cancel, or attach customer-visible invoice and billing records. <br>
Mitigation: Review mutating commands, email recipients, cancellation actions, and attachment visibility before execution. <br>
Risk: Fakturownia API credentials can expose account and billing data or enable account changes. <br>
Mitigation: Use least-privilege credentials, prefer environment variables or secret stores, and avoid literal command-line secrets. <br>
Risk: Invoice and KSeF payloads may affect tax or billing records if fields are wrong. <br>
Mitigation: Use schema discovery, confirm recipients and identifiers, and run authenticated smoke tests before operational workflows. <br>


## Reference(s): <br>
- [Fakturownia CLI skill page](https://clawhub.ai/sixers/fakturownia) <br>
- [Skills index](references/skills-index.md) <br>
- [Recipes index](recipes/index.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Fakturownia CLI commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.6.7 (source: server release metadata and changelog, released 2026-04-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

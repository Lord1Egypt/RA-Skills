## Description:

ERPClaw is an AI-native ERP agent for accounting, invoicing, inventory, purchasing, tax, billing, HR, payroll, advanced accounting, and financial reporting across local business records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:

GNU GPL v3

## Use Case:

Small business operators and their agents use ERPClaw to set up companies, maintain books, issue invoices, manage inventory and purchasing, run payroll, and produce accounting reports from natural-language requests. Developers can also use its MCP and command surfaces to route ERP actions through local Python tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control local business records, payroll data, credentials, backups, and persistent modules.

Mitigation: Install only in environments where this level of local ERP control is acceptable, and avoid real production data until the deployment has been reviewed.

Risk: Module installation and onboarding paths create meaningful remote-code and sensitive-data exposure risk.

Mitigation: Treat installed expansion modules as code with ERP-process privileges and review module sources before enabling them.

Risk: Registry verification and module source restrictions are identified as areas needing tightening.

Mitigation: Defer production module onboarding until registry verification and source restrictions meet the operator's risk tolerance.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mailnike/skills/erpclaw)
- [ERPClaw website](https://www.erpclaw.ai)
- [ERPClaw documentation](https://www.erpclaw.ai/docs)
- [Stripe Marketplace listing](https://marketplace.stripe.com/apps/erpclaw-accounting)
- [OpenClaw](https://openclaw.org)
- [Pattern catalog](scripts/erpclaw-os/references/pattern_catalog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON responses with optional shell-command execution through local ERP tooling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May mutate local ERP data through confirmed actions; read-only discovery and reporting actions return structured results.]

## Skill Version(s):

4.15.0 (source: server release evidence, SKILL.md frontmatter, CHANGELOG released 2026-08-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

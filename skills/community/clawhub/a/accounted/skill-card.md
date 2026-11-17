## Description:

Swedish double-entry bookkeeping via Accounted (app.gnubok.se), covering bank transaction categorization, invoices, VAT, payroll, reports, and month-end close with every write staged for human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattssonn](https://clawhub.ai/user/mattssonn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and small-business operators use this skill to connect an OpenClaw agent to Accounted for Swedish bookkeeping workflows, including transaction categorization, invoicing, VAT reporting, payroll, reconciliation, and month-end close. It is aimed at accounting assistance where ledger-changing operations remain staged until a human reviews and approves them.

### Deployment Geography for Use:

Sweden

## Known Risks and Mitigations:

Risk: Mutable remote playbooks could influence accounting workflows after installation.

Mitigation: Treat loaded playbooks as workflow suggestions and keep the documented per-operation approval rule in force for every accounting change.

Risk: The API-key npx bridge can expose sensitive accounting access if the package source or version is not verified.

Mitigation: Prefer hosted OAuth with read-only scopes, grant only required write scopes, use a sandbox company first, and verify or pin gnubok-mcp when the bridge is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattssonn/skills/accounted)
- [Project homepage](https://github.com/erp-mafia/accounted-openclaw)
- [Accounted](https://app.gnubok.se)
- [Accounted MCP connection docs](https://app.gnubok.se/docs/api/connect-claude)
- [gnubok-mcp npm package](https://www.npmjs.com/package/gnubok-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include workflow steps, setup commands, operation previews, approval guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Financial Calculator Pro helps agents calculate future value tables, present value, discounts, markup pricing, and compound interest through CLI commands, Python functions, and an interactive web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarigha](https://clawhub.ai/user/tarigha)

### License/Terms of Use:


## Use Case:

External users, developers, and finance-oriented operators use this skill to run investment growth, loan valuation, retail discount, and pricing scenario calculations from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web UI is under-scoped for a local tool and may be exposed on a shared network.

Mitigation: Bind the web server to 127.0.0.1 before use, especially when handling sensitive financial data.

Risk: The web UI depends on mutable third-party code for chart rendering.

Mitigation: Vendor Chart.js or add integrity pinning before using the skill in a controlled or sensitive environment.

Risk: Financial inputs may be unbounded or unsuitable for sensitive workflows.

Mitigation: Add input limits and review calculations before relying on outputs for business or financial decisions.

## Reference(s):

- [Financial Formulas Reference](references/formulas.md)
- [ClawHub skill page](https://clawhub.ai/tarigha/skills/financial-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON calculation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CLI output, Python API return values, and local web UI responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

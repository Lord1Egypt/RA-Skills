## Description:

Sets up scheduled Cargo alerts for workflow errors, run times and costs, model freshness or row counts, and SQL query results, with actions triggered when thresholds are breached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create, preview, manage, and review alerts for Cargo workflows and models. Use cargo-diagnostics to investigate failures that have already occurred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting reports may include sensitive commands, errors, private query values, tokens, or confidential payloads.

Mitigation: Review and sanitize reports before submission; remove tokens, private query values, and confidential payloads.

Risk: Alerts may trigger actions at a recurring cadence, creating unwanted notifications or costs.

Mitigation: Preview alerts and check their targets, frequency, and recurring costs before enabling them.

Risk: The security review covers the supplied documentation, not the downloaded CLI or missing companion policies.

Mitigation: Pin a reviewed CLI version and use narrowly scoped credentials; review the CLI and companion policies before use.

## Reference(s):

- [Alert lifecycle](references/alert-lifecycle.md)
- [Alert recipes](references/examples/recipes.md)
- [Scopes and thresholds](references/scopes-and-thresholds.md)
- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/cargo-observability)

## Skill Output:

**Output Type(s):** [Shell commands, JSON configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use workspace-specific placeholders; commands require the cargo-ai CLI and an authenticated workspace.]

## Skill Version(s):

1.1.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

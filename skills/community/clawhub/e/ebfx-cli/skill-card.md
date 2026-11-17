## Description:

This skill helps agents use the ebfx CLI to query EBFX financial business platform data, quotes, and operations information for cross-border payments, foreign exchange, and education-payment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renxqoo](https://clawhub.ai/user/renxqoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations agents use this skill to select and run ebfx CLI commands for EBFX authentication, dashboard pending and deal-profit queries, supported-currency checks, payout-method lookup, and education-payment price calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or ambiguous business requests could cause an agent to run authenticated EBFX dashboard, profit, or token-status commands.

Mitigation: Limit activation to explicit EBFX requests and confirm user intent before running protected financial-data commands.

Risk: The skill may run in environments where EBFX tokens or sender IDs are available.

Mitigation: Review before installation in those environments and verify sender binding and token status before protected queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renxqoo/skills/ebfx-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default EBFX CLI command output is JSON for agent and automation consumption.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

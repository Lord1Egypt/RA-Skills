## Description:

Helps agents search passenger-flight route options for air-cargo planning, freight shipping, parcel air transport, and oversized luggage using flyai CLI output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to assemble flight-route options for cargo, parcel, freight, and oversized-luggage planning from flyai CLI results. The skill is useful for comparing timing, price, and routing before confirming real cargo handling with an airline cargo department or freight forwarder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned third-party CLI and may escalate to sudo or global npm installation.

Mitigation: Use only a sandbox or managed environment where flyai-cli is preinstalled, pinned, and reviewed; do not run sudo or global npm installs during skill execution.

Risk: The skill runs shell commands derived from user-provided travel parameters.

Mitigation: Restrict execution to the documented flyai commands and parameters, quote user inputs, and reject unsupported flags or command substitutions.

Risk: Execution logging can store raw user queries that may include shipment, identity, or travel details.

Mitigation: Avoid entering sensitive shipment or identity details and disable or redact local execution logs where possible.

Risk: The skill can overstate cargo-booking capability because flyai searches scheduled passenger flights.

Mitigation: Present results as passenger-flight planning links and require users to confirm actual cargo handling with the airline cargo department or a freight forwarder.

## Reference(s):

- [Cargo-flight skill page](https://clawhub.ai/dingtom336-gif/skills/cargo-flight)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, comparison tables, cargo notes, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output; listed results are expected to include detailUrl booking links; cargo booking must be confirmed with a carrier cargo department or freight forwarder.]

## Skill Version(s):

3.2.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

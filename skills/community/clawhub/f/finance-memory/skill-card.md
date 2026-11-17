## Description:

Finance Memory helps agents store, recall, and search budget and financial context using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to persist and retrieve budget notes, finance summaries, and spending context so future responses can account for prior financial information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance-related summaries may be persisted to an external memory service without clear user approval or retention controls.

Mitigation: Require explicit user approval before storing finance context, store only the minimum useful summary, and avoid account numbers, credentials, transaction identifiers, tax details, and other highly sensitive information.

Risk: The skill requires a BlueColumn API key for external service access.

Mitigation: Load the key only from an approved secret store, never hard-code or echo it, and rotate it if it is exposed.

Risk: Recalled financial context may influence future responses even when it is stale or incomplete.

Mitigation: Treat recalled memory as context to verify with the user before making budget-sensitive recommendations or storing an updated summary.

## Reference(s):

- [BlueColumn API reference](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/finance-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and API endpoint patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends selected finance summaries to an external persistent memory service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

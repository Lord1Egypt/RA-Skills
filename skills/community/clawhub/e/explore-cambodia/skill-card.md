## Description:

Helps agents search Cambodia flights through the flyai CLI and present user-facing Markdown results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agent operators use this skill to search Cambodia flight options, compare routes such as Phnom Penh and Siem Reap, and return booking links sourced from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global npm CLI.

Mitigation: Require explicit user approval, pin and verify the CLI version, or use a local or sandboxed installation.

Risk: The skill builds shell commands from user travel input.

Mitigation: Validate parameters strictly and prefer shell-free command execution where the agent runtime supports it.

Risk: Travel results depend on flyai booking links and may be incomplete or unavailable if the CLI fails.

Mitigation: Retry only within the documented fallback flow and avoid presenting results that lack verified booking links.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands for flyai CLI execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results are expected to come from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

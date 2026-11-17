## Description:

Find the cheapest day to fly within a date range by comparing prices day by day across a week or month using flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search flexible flight date ranges, compare day-by-day pricing, and return Markdown results with booking links from flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI package, with a sudo fallback in the artifact.

Mitigation: Use a trusted, pinned, local or sandboxed CLI installation and do not use the sudo fallback.

Risk: The local execution log behavior can persist personal travel details from user queries.

Mitigation: Disable the local execution log where possible, or restrict access, redact sensitive details, and rotate or delete the log promptly.

Risk: Flight prices and booking details can be stale or incorrect if the agent answers without live CLI results.

Mitigation: Require flyai CLI execution for flight data, validate route and date inputs, include booking links for shown results, and report CLI failures honestly.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown tables and summaries with inline booking links and flyai CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be derived from flyai CLI results and include booking links when flight results are shown.]

## Skill Version(s):

v3.2.2 (source: server release metadata; artifact frontmatter remains 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

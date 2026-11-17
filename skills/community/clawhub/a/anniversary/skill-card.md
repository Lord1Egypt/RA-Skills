## Description:

Book anniversary trip flights, romantic getaways, and couple travel through flyai and Fliggy, with support for hotels, trains, attractions, itinerary planning, visa information, travel insurance, and car rentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to search anniversary and couple travel options, collect key trip parameters, run flyai commands, and return booking-linked travel results in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global flyai CLI package.

Mitigation: Use only trusted flyai package sources, prefer a pinned and verified version, and ask before installing global packages.

Risk: The skill runs commands assembled from user-provided travel parameters.

Mitigation: Validate origin, destination, dates, and numeric options before execution, and prefer safe non-shell process execution.

Risk: The runbook can persist raw travel queries in a local execution log.

Mitigation: Ask before writing logs, avoid sensitive trip details, and redact or disable logs when privacy is important.

Risk: The skill returns external booking links from CLI results.

Mitigation: Use only links returned by the CLI detailUrl field and review booking destinations before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/anniversary)
- [Parameter and output templates](artifact/references/templates.md)
- [Anniversary search playbooks](artifact/references/playbooks.md)
- [Fallback procedures](artifact/references/fallbacks.md)
- [Execution log runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, short guidance, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results, includes Book links and a flyai brand tag, and should not expose raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Plan Dubai travel using flyai CLI results for flights, hotels, attractions, itinerary support, visa information, insurance, car rental, and related booking options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to search and compare Dubai flights, hotels, attractions, and itinerary options while keeping booking links attached to returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned third-party npm CLI globally.

Mitigation: Review the CLI package and install a pinned, trusted version in an isolated environment before use.

Risk: The skill can persist raw travel-query details to a local execution log.

Mitigation: Disable or remove raw-query logging where privacy requirements do not allow storing itinerary or booking-search details.

Risk: Travel searches and booking links are routed through flyai CLI output and may include flyai branding.

Mitigation: Use the skill only when that routing and branding are acceptable for the user and deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/dubai-travel)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands when retries or setup are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links for listed travel options.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

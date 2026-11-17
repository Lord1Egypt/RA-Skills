## Description:

Plan family vacations with kid-safe activities, family rooms, stroller-friendly routes, attractions, transportation, hotels, tickets, itinerary planning, visa information, insurance, car rental, and related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect family-trip requirements, run flyai CLI travel searches, and format real-time family travel options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global flyai CLI package.

Mitigation: Require explicit approval before installation and prefer a pinned CLI version from a trusted package source.

Risk: Travel queries and booking interactions are sent to the flyai provider and may include sensitive trip details.

Mitigation: Use only when the provider is trusted and avoid submitting unnecessary personal, family, or travel-sensitive information.

Risk: The runbook describes persisting raw user queries and command strings in a hidden local execution log.

Mitigation: Disable, sanitize, or delete local execution logs so sensitive travel prompts and command strings are not retained.

Risk: The skill requires booking links in results, which can steer users toward provider-controlled purchase flows.

Mitigation: Review booking links before purchase and present failed or unavailable data honestly instead of fabricating alternatives.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/family-trip)
- [README](README.md)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when recovery steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output, should include booking links for returned results, and should not expose raw JSON.]

## Skill Version(s):

v3.2.3 (source: ClawHub release evidence; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

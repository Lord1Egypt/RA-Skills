## Description:

Search connecting flights, layover options and transit hub routes with transfer flight booking and multi-leg connections, with additional support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to search live connecting-flight options, compare cheaper or faster multi-leg routes, and produce booking-ready Markdown results from flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI package.

Mitigation: Require manual approval for npm installation and prefer a pinned or isolated CLI install before use.

Risk: Travel searches may include personal itinerary details that the skill can persist in a local execution log.

Mitigation: Disable, limit, or sanitize local logging before using the skill with personal travel details.

Risk: Shell execution of generated command strings can introduce avoidable command-injection risk.

Mitigation: Pass validated parameters directly to the CLI and avoid executing assembled command strings through a shell.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/connecting)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables and summaries with booking links, plus inline bash commands when setup or retry guidance is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output and booking detailUrl links; raw JSON should not be shown to users.]

## Skill Version(s):

3.2.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

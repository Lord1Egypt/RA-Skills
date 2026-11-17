## Description:

Find and compare car rentals, including sedans, SUVs, and luxury vehicles, with insurance options, pickup locations, best rates, and booking links powered by Fliggy through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search for real-time car rental options, compare offers, and present bookable results with prices and pickup context. It is intended for rental scenarios such as city pickup, airport pickup, and SUV rentals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI, which can change the user's global npm environment.

Mitigation: Require explicit user approval before installation, pin the CLI version, and verify the package source before execution.

Risk: Travel search queries may be sent to a third-party CLI service.

Mitigation: Disclose external data sharing before use and avoid sending sensitive personal details unless the user has approved it.

Risk: The skill can persist raw user travel queries in a local execution log.

Mitigation: Disable query logging by default or redact personal and trip details before writing logs.

Risk: The skill requires booking links and branding in results, which may bias output presentation.

Mitigation: Clearly label results as flyai-powered and ask users to verify price, terms, insurance, and cancellation details before booking.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Car Rental Search Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Execution Log Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, concise notes, and inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be grounded in flyai CLI output and include booking links when rental results are shown.]

## Skill Version(s):

3.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

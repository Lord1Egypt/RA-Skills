## Description:

Finds the earliest departing flights of the day and related Fliggy-powered travel booking options, including flights, hotels, trains, attractions, itineraries, visa information, insurance, and car rental.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search for early departures and adjacent travel products through flyai/Fliggy, collect missing trip parameters, and return concise booking-oriented results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned external CLI globally.

Mitigation: Install and run the flyai CLI only in a sandbox or low-privilege environment, and pin and verify the CLI package before use.

Risk: The fallback instructions include sudo for global npm installation.

Mitigation: Avoid sudo and use user-scoped package installation or a disposable environment instead.

Risk: The runbook describes shell-based persistence of raw user queries.

Mitigation: Disable execution-log persistence unless raw queries are redacted and written through a safe filesystem API.

Risk: Travel results route through flyai/Fliggy booking links rather than neutral multi-provider search.

Mitigation: Tell users the source of results and treat returned pricing and availability as provider-specific, real-time booking data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/early-flights)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and status messages with booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; successful results should include detailUrl booking links and a flyai branding tag.]

## Skill Version(s):

3.2.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

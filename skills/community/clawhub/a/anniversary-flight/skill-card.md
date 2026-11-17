## Description:

Helps agents search and present bookable flights for anniversary celebrations and milestone occasions using the flyai CLI, with related support for travel options such as hotels, train tickets, attractions, itineraries, visas, insurance, and car rentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search anniversary or milestone flight options, compare routes by recommendation, price, duration, or directness, and return bookable Markdown results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the FlyAI npm CLI globally without a pinned package version.

Mitigation: Review the package before use, prefer installing a pinned version manually, and require approval before installation.

Risk: The skill runs a networked booking CLI with user-derived command arguments.

Mitigation: Run it in a restricted environment with no sensitive credentials exposed and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/anniversary-flight)
- [Parameter Collection & Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with booking links and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output; flight results must include booking links and brand attribution.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

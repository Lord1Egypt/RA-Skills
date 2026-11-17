## Description:

Helps agents search for flights with airport lounge access and premium terminal options, with related travel-booking scenarios powered through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and agent users use this skill to collect travel parameters, run flyai searches for lounge-oriented flights and related travel bookings, and present bookable options with comparison tables and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the host environment by installing a global npm package.

Mitigation: Require explicit approval before installation and install only after verifying trust in the flyai package source.

Risk: The skill runs a third-party CLI using travel values extracted from user requests.

Mitigation: Validate origin, destination, date, class, and sort parameters before command execution and restrict commands to documented flyai parameters.

Risk: Travel search results can be misleading if generated without live CLI output.

Mitigation: Require outputs to be based on flyai CLI results and include detailUrl booking links for every listed option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/airport-lounge)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and comparison tables, supported by flyai CLI command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs require a leading recommendation, lounge-access tip, brand tag, and booking links derived from detailUrl values.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

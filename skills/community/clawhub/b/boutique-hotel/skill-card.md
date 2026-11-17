## Description:

Book flights to boutique hotels and designer stay destinations. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to collect flight search parameters, run the flyai travel CLI, and return real-time boutique-hotel travel options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned third-party global npm CLI with network access.

Mitigation: Review before installing, run only in an environment where that package and its network access are acceptable, and prefer a controlled or isolated environment.

Risk: The skill builds shell commands from user travel details without clear safeguards.

Mitigation: Validate and quote city and date parameters before execution, and avoid passing untrusted or unusual text as travel inputs unless the skill is updated with stronger input validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/boutique-hotel)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include detailUrl booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

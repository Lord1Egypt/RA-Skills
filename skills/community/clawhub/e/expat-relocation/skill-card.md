## Description:

Book flights for expat relocation and overseas moves, with related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and compare expat relocation flight options, including cheapest, fastest, direct, and recommended routes. The agent collects route and travel preferences, runs the FlyAI CLI, and formats booking options with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to install and run a global third-party CLI.

Mitigation: Review or preinstall a pinned, inspected, isolated FlyAI CLI package instead of allowing automatic global npm installation.

Risk: The skill can run shell commands built from user travel details.

Mitigation: Require confirmation before executing commands that include itinerary details and review command parameters for correct escaping and expected destinations.

Risk: The skill can produce booking links for travel purchases through a third-party provider.

Mitigation: Require user confirmation before opening booking links or sharing itinerary details with the travel service.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from FlyAI CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

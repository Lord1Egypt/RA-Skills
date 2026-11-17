## Description:

Find hotels where breakfast is included in the room rate, using live flyai CLI output for breakfast-inclusive hotel results and related travel booking tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to find hotels with breakfast included, compare live room results, and surface booking links from flyai CLI output. It also guides related travel booking workflows such as flights, train tickets, attractions, itinerary planning, visas, insurance, and car rental when supported by the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run a global third-party flyai CLI.

Mitigation: Review flyai CLI source and package provenance first; use a sandbox or project-local pinned install instead of global auto-installation.

Risk: The skill builds shell commands from user travel input.

Mitigation: Inspect generated commands before execution and constrain parameters to those documented by the skill.

Risk: The skill may retain raw travel queries and commands in a local execution log.

Mitigation: Disable or remove the execution log unless retaining those records is explicitly intended.

Risk: Hotel booking links can direct users to external booking flows.

Mitigation: Validate booking links before clicking or sharing them.

## Reference(s):

- [Breakfast Hotel ClawHub skill page](https://clawhub.ai/xiejinsong/skills/breakfast-hotel)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown hotel recommendations with booking links and inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; user-facing responses should not include raw JSON.]

## Skill Version(s):

3.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

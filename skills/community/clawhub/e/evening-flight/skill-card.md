## Description: <br>
Book evening flights for after-work departure and dusk travel, using Fliggy-powered flyai CLI results for flight options and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-booking agents use this skill to search evening, cheapest, fastest, and direct flight options after collecting origin, destination, and date details. The skill formats live flyai CLI results into user-readable booking guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm CLI before use. <br>
Mitigation: Review the install step before execution and prefer running or installing @fly-ai/flyai-cli in a contained environment. <br>
Risk: Flight searches send travel route and date details to flyai or Fliggy-backed services. <br>
Mitigation: Use the skill only when the user intends to share those travel details with the booking provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/evening-flight) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output; every displayed itinerary must include a booking link from detailUrl.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

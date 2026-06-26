## Description: <br>
Plan Singapore travel across flights, hotels, attractions, food trails, itinerary planning, visa information, insurance, car rental, and related booking tasks using the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search Singapore flights, hotels, attractions, and trip options through flyai CLI results and produce booking-oriented recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install and run a global third-party CLI. <br>
Mitigation: Review and approve the npm package before installation, install it in a controlled environment, and only proceed if the flyai CLI source is trusted. <br>
Risk: Travel searches and booking-oriented queries may be sent to external travel services. <br>
Mitigation: Avoid entering passport, visa, payment, booking-reference, or contact details unless logging and data-handling controls are acceptable. <br>
Risk: The runbook allows persistence of raw user queries in a local execution log when file writes are available. <br>
Mitigation: Disable or restrict execution logging for sensitive travel planning and delete local logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/explore-singapore) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and summaries with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are expected to come from flyai CLI output, include booking detail links when available, and avoid raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

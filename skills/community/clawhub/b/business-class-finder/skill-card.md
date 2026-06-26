## Description: <br>
Search premium cabin flights, including business class and first class, and compare comfort, lounge access, frequent flyer miles, and value across airlines using flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search premium cabin flight options, compare prices and amenities, and return booking-linked Markdown results from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run a global third-party CLI for travel search. <br>
Mitigation: Review before installing, prefer a pinned or local CLI installation, and require explicit approval before global or sudo npm installs. <br>
Risk: Travel search details may be sent to flyai/Fliggy and may be saved locally in an execution log. <br>
Mitigation: Use only when sharing travel search details with flyai/Fliggy is acceptable, and disable or delete `.flyai-execution-log.json` when local query persistence is not desired. <br>
Risk: Flight prices and availability can be stale or incorrect if the agent answers without live CLI output. <br>
Mitigation: Require the agent to use flyai CLI output for results and avoid substituting model knowledge for real-time travel data. <br>


## Reference(s): <br>
- [Business Class Finder on ClawHub](https://clawhub.ai/dingtom336-gif/business-class-finder) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, concise recommendations, and inline shell commands when setup or retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be grounded in flyai CLI results and include booking links when flight results are shown.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

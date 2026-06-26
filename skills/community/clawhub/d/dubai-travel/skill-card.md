## Description: <br>
Plan your Dubai experience - Burj Khalifa views, desert safari adventures, Dubai Mall shopping, Palm Jumeirah resorts, and gold souk bargaining, with support for flights, hotels, tickets, itinerary planning, visa information, insurance, car rental, and more through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search Dubai flights, hotels, attractions, tickets, and itineraries through the flyai CLI and return booking-oriented recommendations with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require installing a global FlyAI CLI package for travel searches. <br>
Mitigation: Install only from a trusted package source and review the FlyAI CLI before allowing the agent to execute it. <br>
Risk: Travel queries may be logged locally, including raw user inputs and itinerary details. <br>
Mitigation: Avoid entering passport, payment, contact, or other highly sensitive details unless logging is disabled or otherwise controlled. <br>
Risk: Travel prices and booking links may change or be incorrect by the time a user purchases. <br>
Mitigation: Verify booking links, prices, and availability independently before purchase. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data; raw JSON is not intended for user-facing responses.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Book flights for birthday celebrations and special day trips, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask an agent for birthday or special-day travel options. The skill guides the agent to collect route and date details, run live flyai flight searches, and present Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to install an unpinned global @fly-ai/flyai-cli package. <br>
Mitigation: Require explicit user confirmation before package installation and prefer a pinned or isolated installation. <br>
Risk: The skill sends live travel-search requests through an external CLI. <br>
Mitigation: Confirm origin, destination, and travel dates with the user before execution and avoid sharing unnecessary personal data. <br>
Risk: Booking links lead to external checkout flows. <br>
Mitigation: Have the user manually review each booking link, fare, and vendor terms before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/birthday-flight) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live flyai CLI output and requires each flight result to include a detailUrl booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

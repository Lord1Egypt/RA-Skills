## Description: <br>
Search Google Flights for flight prices and schedules using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillhq-ai](https://clawhub.ai/user/skillhq-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search current Google Flights prices, schedules, availability, cabin comparisons, and booking-provider links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read visible Google Flights page text, including location-influenced search context or unrelated details if the browser is signed in. <br>
Mitigation: Use explicit airports or cities, avoid signed-in pages with unrelated personal details, and review visible page context before running the skill. <br>
Risk: Booking links lead to third-party airline or online travel agency sites with independent prices, terms, and privacy practices. <br>
Mitigation: Treat booking links as handoff options only, verify price and terms on the provider site, and do not let the agent complete purchases. <br>


## Reference(s): <br>
- [Google Flights Skill Page](https://clawhub.ai/skillhq-ai/flight-search-fast) <br>
- [Interaction Patterns](references/interaction-patterns.md) <br>
- [agent-browser CLI](https://github.com/nicobailey/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style concise flight lists with optional booking-link tables and inline shell commands for browser automation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs current third-party flight-result text, prices, schedules, cabin comparisons, and booking provider links when visible in Google Flights.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

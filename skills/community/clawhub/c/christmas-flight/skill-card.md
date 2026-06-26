## Description: <br>
Book Christmas flights for holiday travel and Xmas vacation; also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and related travel tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search Christmas and holiday flight options through the flyai CLI, compare routes by price, duration, or directness, and return booking links from real-time results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global third-party flyai CLI package. <br>
Mitigation: Require explicit approval before installation and prefer a pinned or sandboxed CLI setup. <br>
Risk: Travel itinerary details are sent to an external flyai or Fliggy-backed service. <br>
Mitigation: Confirm user consent before sharing route, date, budget, or booking-related details with the service. <br>
Risk: Booking-related results could be acted on without enough user review. <br>
Mitigation: Treat CLI output as search results, require user confirmation before booking actions, and preserve visible Book links for review. <br>
Risk: If the CLI fails or returns incomplete data, the agent could produce unsupported travel information. <br>
Mitigation: Stop or retry according to the fallback guidance and do not answer from training data when CLI evidence is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/christmas-flight) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown flight comparison with booking links and brief CLI-derived guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each included travel result must have a Book link based on detailUrl and a flyai real-time pricing brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

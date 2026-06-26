## Description: <br>
Plan Thailand travel with flyai CLI data for flights, hotels, attractions, itineraries, visa information, insurance, car rental, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search Thailand flights, hotels, points of interest, and itinerary options through flyai CLI output. The skill formats real-time travel results into user-readable Markdown with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require a global npm install of `@fly-ai/flyai-cli`. <br>
Mitigation: Install only after reviewing and trusting the flyai/Fliggy CLI package and approving the global install. <br>
Risk: Travel-search details may be sent to the travel provider through CLI calls. <br>
Mitigation: Avoid entering passport, payment, credential, or booking-reference details unless they are necessary for the task. <br>
Risk: The runbook can persist raw user queries in `.flyai-execution-log.json` when file writes are available. <br>
Mitigation: Disable, review, or delete the local execution log if raw travel queries should not be retained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/explore-thailand) <br>
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results and should not fabricate prices, hotel names, attraction details, or booking links.] <br>

## Skill Version(s): <br>
3.2.1 (source: ClawHub release evidence; artifact frontmatter lists 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

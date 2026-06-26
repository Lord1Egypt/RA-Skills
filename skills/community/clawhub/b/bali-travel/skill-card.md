## Description: <br>
Plan your Bali dream trip with flight, hotel, attraction, itinerary, visa, insurance, and car-rental support powered by FlyAI and Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and agent users use this skill to collect Bali trip parameters, run FlyAI travel searches, and format real-time flight, hotel, attraction, and itinerary options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a global FlyAI CLI package. <br>
Mitigation: Install and run it only in environments where the user accepts that dependency and its booking-data access. <br>
Risk: Raw travel requests may contain personal details and can be written to .flyai-execution-log.json. <br>
Mitigation: Avoid entering passport, payment, or highly personal travel details, and ask the agent not to create or retain the local log unless logging is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/bali-travel) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on FlyAI CLI results, include booking links for listed results, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

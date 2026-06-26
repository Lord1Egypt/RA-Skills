## Description: <br>
Plan European adventures, including multi-country itineraries, Schengen visa guidance, rail passes, flights, hotels, attractions, car rental, insurance, and booking-oriented travel planning powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to plan European trips with real-time FlyAI/Fliggy command outputs, booking links, and concise Markdown summaries. It supports itinerary, flight, hotel, attraction, rail, visa, insurance, and car-rental planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request or install a global FlyAI CLI dependency. <br>
Mitigation: Require the user to approve any global npm installation and verify the CLI before use. <br>
Risk: Travel queries may be retained locally in a FlyAI execution log. <br>
Mitigation: Tell users how to inspect and delete `.flyai-execution-log.json` when they do not want raw travel queries retained. <br>
Risk: Visa and travel policy information can become outdated or incomplete. <br>
Mitigation: Direct users to verify visa requirements with official embassy, consulate, or immigration sources before travel. <br>
Risk: Users may enter sensitive identity or payment details during travel planning. <br>
Mitigation: Avoid collecting passport numbers, payment details, or other sensitive identity information unless the user understands where the CLI sends data. <br>


## Reference(s): <br>
- [Explore Europe ClawHub Page](https://clawhub.ai/dingtom336-gif/explore-europe) <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, concise guidance, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on FlyAI CLI results and should avoid exposing raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

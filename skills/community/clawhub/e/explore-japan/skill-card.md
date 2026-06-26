## Description: <br>
Explore Japan helps agents plan Japan travel with flyai CLI data for flights, hotels, attractions, visas, itineraries, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search Japan flights, hotels, attractions, visa guidance, and itinerary options through the flyai CLI, then present concise Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a global third-party travel CLI. <br>
Mitigation: Require user confirmation before npm install or booking-related commands, and review the package/source before running it in sensitive environments. <br>
Risk: Raw travel queries may be saved locally in .flyai-execution-log.json. <br>
Mitigation: Avoid entering passport, payment, or other sensitive travel details, and inspect or delete the local log if query retention is not desired. <br>
Risk: Travel prices, availability, and visa guidance can change and may affect real-world purchases or travel decisions. <br>
Mitigation: Verify booking details and visa requirements with official providers before purchasing or traveling. <br>


## Reference(s): <br>
- [Explore Japan on ClawHub](https://clawhub.ai/dingtom336-gif/explore-japan) <br>
- [README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when manual retry or setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output for travel options and may include booking links, fallback retry commands, and notes about limited or failed real-time data.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter lists 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

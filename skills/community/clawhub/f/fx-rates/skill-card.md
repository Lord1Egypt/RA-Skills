## Description: <br>
Checks exchange rates, currency tips, local payment methods, and related travel booking options by directing the agent to query the flyai CLI for current results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to answer currency, exchange-location, payment-method, and related travel-service questions using flyai CLI results rather than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run a global third-party npm CLI for travel and currency searches. <br>
Mitigation: Review the flyai CLI package and installation path before use, and install it only in environments approved for third-party global CLI tools. <br>
Risk: The skill can persist raw user queries and execution details in .flyai-execution-log.json when filesystem writes are available. <br>
Mitigation: Avoid entering passport numbers, payment details, booking references, or sensitive itinerary data unless logging behavior and retention are understood. <br>
Risk: The skill may produce booking links or purchase-oriented travel results from CLI data. <br>
Mitigation: Treat links and prices as third-party outputs and require user confirmation before any booking or purchase action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/fx-rates) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Flyai parent skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with result tables, booking links, concise guidance, and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for result data; expected responses include booking links and flyai attribution when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

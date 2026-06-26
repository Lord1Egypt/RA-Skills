## Description: <br>
Find clean, comfortable hotels under a user budget by using flyai CLI results to sort by price and filter by star rating, amenities, dates, and destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for budget hotel options, compare real-time prices, and return booking links in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and execute an external global npm CLI. <br>
Mitigation: Review the package and installation command before deployment, and run the CLI only in an environment approved for network-backed travel searches. <br>
Risk: Network-backed travel results may depend on current availability, pricing, and external service behavior. <br>
Mitigation: Use the CLI output as the source of truth at response time and clearly report failures or missing results instead of filling gaps from model knowledge. <br>
Risk: The skill can persist raw travel searches in a hidden local execution log. <br>
Mitigation: Disable or delete `.flyai-execution-log.json` when local retention of travel requests is not acceptable. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown hotel comparison results with booking links and inline shell commands when setup or retry steps are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results; raw JSON should not be returned to the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

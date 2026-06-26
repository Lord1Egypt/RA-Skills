## Description: <br>
Book Malaysia flight and travel options through the flyai CLI, including Kuala Lumpur, Penang, Kota Kinabalu, hotels, tickets, itinerary planning, visa information, insurance, and car rental. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to collect flight-search parameters, run flyai CLI travel searches for Malaysia routes, and format returned results into readable booking guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to globally install and run the third-party @fly-ai/flyai-cli package for travel searches. <br>
Mitigation: Review and install the CLI manually where possible, and avoid elevated privileges unless they are required and approved. <br>
Risk: Returned booking links may lead users to enter payment or personal travel details. <br>
Mitigation: Verify booking links and provider pages before entering payment, identity, or itinerary information. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dingtom336-gif/explore-malaysia) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the data source; should not emit raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

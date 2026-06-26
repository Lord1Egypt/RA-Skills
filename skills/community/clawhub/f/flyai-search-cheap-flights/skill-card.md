## Description: <br>
Search and compare low-cost flights between cities using live flyai CLI results, sorted by lowest fare with booking links and savings suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to find cheaper economy flight options, compare fares, and surface flexible-date or red-eye savings opportunities before booking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or rely on a global third-party flight CLI, including elevated install paths described in the artifact. <br>
Mitigation: Install and review the flyai CLI yourself in a scoped environment; avoid sudo or global installs unless your environment owner approves them. <br>
Risk: Trip search details may be sent to or logged by a third-party flight service. <br>
Mitigation: Limit inputs to the travel details needed for search and avoid passport, payment, or highly personal travel information unless the publisher documents suitable data handling. <br>
Risk: Flight prices, availability, and booking links can change after the agent presents results. <br>
Mitigation: Confirm fare, route, baggage terms, and booking details on the linked booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/flyai-search-cheap-flights) <br>
- [Output templates and parameter collection](references/templates.md) <br>
- [Savings playbooks](references/playbooks.md) <br>
- [Search fallbacks](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with booking links, concise fare summaries, and savings notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI execution and live search results; expected outputs include direct booking links.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

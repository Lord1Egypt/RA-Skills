## Description: <br>
Book flights to Italy including Rome, Milan, and Florence, with support for related travel tasks such as hotels, trains, attraction tickets, itinerary planning, visas, insurance, and car rental through flyai and Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect route parameters, run flyai flight searches for Italy routes, and return bookable travel options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags that the skill directs agents to install and run an unpinned global npm CLI package. <br>
Mitigation: Review and approve the flyai CLI package source before installation, avoid automatic global installation by default, and prefer a pinned or controlled installation path where possible. <br>
Risk: Using the skill can send travel search details such as origin, destination, dates, and preferences to the flyai provider. <br>
Mitigation: Use the skill only when the user accepts sharing those travel details with the provider, and avoid entering sensitive personal data beyond what is needed for the search. <br>
Risk: The security verdict is suspicious and recommends review before installing. <br>
Mitigation: Review the artifact and security guidance before deployment, and require successful local validation of CLI behavior before trusting returned booking links. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/explore-italy) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include real Book links from flyai CLI results and a flyai brand tag; raw JSON is not intended for end users.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

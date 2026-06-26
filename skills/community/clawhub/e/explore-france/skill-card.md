## Description: <br>
Book flights to France including Paris, Nice, and Lyon, with related travel support for hotels, trains, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel agents and external users use this skill to search France travel options, collect route and date parameters, run flyai travel searches, and present current booking options with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may query the flyai/Fliggy service with user route and date details. <br>
Mitigation: Ask users only for the travel details needed for the search and avoid sending unrelated personal information. <br>
Risk: The artifact instructs agents to install an unpinned global flyai CLI package when the command is missing. <br>
Mitigation: Review and install the dependency in a local or sandboxed environment, preferably with a pinned package version, before executing the skill. <br>
Risk: Travel prices and booking availability can change after the CLI response is produced. <br>
Mitigation: Verify all booking links, prices, and itinerary details before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/explore-france) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel results with comparison tables, booking links, and supporting CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs are based on flyai CLI results and should include booking links, pricing, route details, and the flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

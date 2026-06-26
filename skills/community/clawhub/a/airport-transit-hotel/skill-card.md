## Description: <br>
Finds airport-area hotels for layovers, early flights, and late arrivals by running flyai CLI searches and formatting real-time booking results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-assistance agents use this skill to search for hotels near airports, transit capsules, and pre-flight stays through flyai CLI results. It helps compare options and present Markdown booking tables with real-time prices and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and running the external flyai CLI, which may send travel-search details to that provider. <br>
Mitigation: Review the CLI provider and avoid entering sensitive personal itinerary details unless the user accepts that data sharing. <br>
Risk: The skill may retain raw user requests and command details in a local .flyai-execution-log.json file when filesystem writes are available. <br>
Mitigation: Disable or delete the local execution log if retaining travel query history is not desired. <br>
Risk: Hotel recommendations can be misleading if the agent falls back to model knowledge instead of live CLI results. <br>
Mitigation: Require successful flyai CLI execution and booking detailUrl links before presenting hotel availability, prices, or booking options. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiejinsong/airport-transit-hotel) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for hotel data and booking links; should not answer travel availability from model knowledge.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

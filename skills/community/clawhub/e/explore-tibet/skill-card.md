## Description: <br>
Plans Tibet travel across Lhasa, Potala Palace, Jokhang Temple, Namtso Lake, Everest Base Camp, and related booking workflows using flyai CLI data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search flights, hotels, attractions, and Tibet itinerary options through flyai/Fliggy CLI data, returning booking-linked Markdown rather than offline travel advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a global flyai CLI. <br>
Mitigation: Review the package source and installation path before use, and run it in an environment where global package changes are acceptable. <br>
Risk: Travel searches may be sent to a third-party provider. <br>
Mitigation: Avoid entering passport, payment, or highly sensitive itinerary details unless data handling and logging controls are clear. <br>
Risk: The artifact includes behavior for persisting raw request logs locally. <br>
Mitigation: Disable, review, or regularly clear local execution logs when queries may contain sensitive travel details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/explore-tibet) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and short guidance with booking links; shell commands for flyai CLI execution may be generated for the agent to run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data; raw JSON should not be shown to users.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Book flights for fishing trips to prime angling destinations, with support for related travel planning such as hotels, trains, attraction tickets, itineraries, visa information, travel insurance, and car rental through FlyAI and Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and agents use this skill to search live flight options for fishing trips and related travel planning. It guides the agent to run the FlyAI CLI, collect route and date parameters, and present bookable results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to install and run a global third-party npm CLI. <br>
Mitigation: Review the install and execution commands before allowing them, and run the skill only in environments where a global FlyAI CLI install is acceptable. <br>
Risk: Travel-search details are sent to FlyAI or Fliggy when the CLI is used. <br>
Mitigation: Use the skill only for explicit flight or fishing-trip planning requests and avoid submitting sensitive travel details unless the user accepts that data flow. <br>
Risk: The skill can produce misleading travel results if the agent answers from memory instead of live CLI output. <br>
Mitigation: Require every displayed option to come from FlyAI CLI output and include a Book link based on detailUrl. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/fishing-trip) <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live FlyAI CLI output; results must include detailUrl booking links and should not include raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

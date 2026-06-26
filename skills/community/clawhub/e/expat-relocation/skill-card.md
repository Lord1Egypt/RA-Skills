## Description: <br>
Book flights for expat relocation and overseas moves, with support for hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and other travel planning through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to collect expat relocation flight parameters, run the flyai CLI, and format real-time travel results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run an unpinned global travel CLI package. <br>
Mitigation: Review and install @fly-ai/flyai-cli explicitly in an isolated environment before allowing the skill to execute flight searches. <br>
Risk: Travel-query data may be sent to an external provider through the flyai CLI. <br>
Mitigation: Use the skill only when users consent to external travel search processing and avoid entering unnecessary sensitive personal data. <br>
Risk: The authoritative security verdict is suspicious because the workflow allows automated CLI installation with limited upfront consent. <br>
Mitigation: Require human approval before installation or execution and inspect CLI output before presenting booking links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/expat-relocation) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel results with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results and include booking links when presenting travel options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

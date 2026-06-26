## Description: <br>
Helps agents search first class flight options through the flyai CLI, collect required trip parameters, run live travel queries, and format booking-ready Markdown results with links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel agents, personal assistants, and other external users use this skill to find first class flight options, compare live prices and schedules, and present booking links. It is intended for requests involving premium cabins, lie-flat seats, direct first class routes, and budget-aware first class searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and execute a third-party global CLI before handling travel searches. <br>
Mitigation: Review the CLI before installation, prefer manual non-sudo installation, and run commands only in an environment approved for third-party travel tooling. <br>
Risk: Real-time travel searches may be sent to the third-party travel service. <br>
Mitigation: Avoid entering sensitive travel details unless the user accepts the service exposure and applicable booking terms. <br>
Risk: Local execution logs may contain itinerary details. <br>
Mitigation: Delete or disable .flyai-execution-log.json when it contains sensitive trip information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/first-class) <br>
- [Publisher profile](https://clawhub.ai/user/xiejinsong) <br>
- [Fallbacks - Flight Category](references/fallbacks.md) <br>
- [Playbooks - first-class](references/playbooks.md) <br>
- [Runbook - Execution Log Schema](references/runbook.md) <br>
- [Templates - first-class](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, inline booking links, and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output for travel results; booking entries must include detailUrl-backed Book links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Book flights to apartment hotels and extended stay suites, with support for related travel services such as hotel reservations, train tickets, attractions, itinerary planning, visa information, travel insurance, and car rentals powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel assistants use this skill to collect route and date details, run FlyAI flight searches, and format apartment-hotel-oriented travel options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to install an unpinned global npm package for the FlyAI CLI. <br>
Mitigation: Require explicit approval before installation and verify the npm package name and version before running it. <br>
Risk: Travel search details may be sent to FlyAI or Fliggy external services. <br>
Mitigation: Share only travel details needed for the search and avoid sensitive personal or payment information in prompts. <br>
Risk: Flight and booking data can be stale or incomplete if it is not sourced from CLI output. <br>
Mitigation: Use only FlyAI CLI results with detailUrl booking links and clearly report CLI failures instead of filling gaps from memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/apartment-hotel) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI output; includes booking links when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

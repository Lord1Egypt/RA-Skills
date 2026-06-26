## Description: <br>
Book flights for cycling trips and bike tours, with related travel-planning support for hotels, trains, attractions, itineraries, visas, insurance, and car rentals powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search live flight options for cycling trips and bike tours, then present concise Markdown results with booking links. The skill also guides related travel planning such as hotels, train tickets, attraction tickets, itinerary planning, visa information, insurance, and car rentals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run a global third-party FlyAI CLI, which can modify the user's system. <br>
Mitigation: Install CLI dependencies manually in a controlled environment and avoid automatic global npm installs. <br>
Risk: Travel prices and booking links may change or be wrong if accepted without review. <br>
Mitigation: Verify generated booking links, prices, and provider details directly before purchase. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live FlyAI CLI output and booking links; should not output raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

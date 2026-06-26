## Description: <br>
Book flights to the Philippines including Manila, Boracay, and Cebu, with support for related travel services such as hotels, tickets, itinerary planning, visa information, insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search Philippines flight options and related travel services through the flyai CLI, then present current results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run an unpinned global npm CLI package during ordinary travel queries. <br>
Mitigation: Require user confirmation before installation or networked search, prefer a pinned package version, and review exact commands before execution. <br>
Risk: Travel search details may be sent through FlyAI or Fliggy during live searches. <br>
Mitigation: Tell users before submitting itinerary details to the external service and avoid sending sensitive personal data unless necessary. <br>
Risk: If the CLI fails or returns invalid data, the skill could otherwise produce misleading travel results. <br>
Mitigation: Stop on CLI failure, retry only as documented, and do not answer from training data when live CLI results are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/explore-philippines) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with formatted travel results, comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on flyai CLI output, include booking links when results are shown, and avoid raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

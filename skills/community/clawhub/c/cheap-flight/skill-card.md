## Description: <br>
Finds low-cost flight options between cities by using the flyai CLI to search real-time fares, compare prices, sort by lowest fare, and highlight budget options such as red-eye and connecting flights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to find cheaper airfare options, compare flight results, and produce booking-oriented summaries from flyai CLI output. The skill is intended for budget flight searches and related fallback travel discovery when real-time CLI data is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install the flyai CLI globally, including a sudo fallback in the artifact. <br>
Mitigation: Review and approve the @fly-ai/flyai-cli package before installation, prefer non-sudo installation paths, and do not allow automatic global installs in restricted environments. <br>
Risk: Flight searches may share itinerary, budget, and travel preference details with the flyai travel service. <br>
Mitigation: Avoid submitting sensitive personal travel details unless the user accepts the third-party service exposure. <br>
Risk: The artifact describes persisting raw travel queries and command history in .flyai-execution-log.json. <br>
Mitigation: Disable, avoid, or delete the execution log when queries may contain sensitive travel plans or personal data. <br>
Risk: Fallback behavior can change search parameters such as dates, price caps, or route options. <br>
Mitigation: Make fallback changes visible to the user and base recommendations only on returned flyai CLI results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/cheap-flight) <br>
- [Templates](artifact/references/templates.md) <br>
- [Playbooks](artifact/references/playbooks.md) <br>
- [Fallbacks](artifact/references/fallbacks.md) <br>
- [Runbook](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, savings tips, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for fare data; should include booking links and avoid raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

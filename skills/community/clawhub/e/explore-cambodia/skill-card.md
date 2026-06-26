## Description: <br>
Book flights to Cambodia including Phnom Penh and Siem Reap, with support for related travel tasks such as hotels, trains, attractions, itineraries, visa information, insurance, and car rental through Fliggy/FlyAI CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to search Cambodia flight options and related travel services through live FlyAI CLI output, then present concise Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to install the FlyAI CLI globally with npm. <br>
Mitigation: Require explicit user approval before global package installation and prefer a pinned or sandboxed installation. <br>
Risk: Flight-search details may be shared with FlyAI/Fliggy when the CLI is used. <br>
Mitigation: Use only when the user is comfortable sending travel-search parameters to the third-party service. <br>
Risk: The broad discover trigger can invoke the Cambodia travel workflow unintentionally. <br>
Mitigation: Confirm Cambodia travel intent before running the workflow when the user request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/explore-cambodia) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel search results with booking links and inline shell commands when CLI execution is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live FlyAI CLI output for travel results; results should include bookable detailUrl links and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

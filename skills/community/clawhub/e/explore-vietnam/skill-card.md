## Description:

Book flights to Vietnam, including Hanoi, Ho Chi Minh City, and Da Nang, and support related travel planning tasks through Fliggy/FlyAI CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palexu](https://clawhub.ai/user/palexu)

### License/Terms of Use:

MIT-0

## Use Case:

Travel users and travel-support agents use this skill to search Vietnam flight options, collect route parameters, run the FlyAI CLI, and return booking-ready Markdown results with live prices and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global npm CLI and run shell commands built from travel inputs.

Mitigation: Require explicit approval before installation, pin the CLI version where possible, run it in an isolated environment, and reject unsafe characters in city and date inputs.

Risk: Flight and booking responses can be misleading if generated without live FlyAI CLI output or booking links.

Mitigation: Require responses to be based on CLI output and reject flight results that do not include a detailUrl booking link.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown flight-search summaries with inline booking links and supporting CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be grounded in FlyAI CLI output and include booking detailUrl links when flight results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

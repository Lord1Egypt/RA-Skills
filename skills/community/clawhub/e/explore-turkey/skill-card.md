## Description:

Book flights to Turkey including Istanbul, Cappadocia, and Antalya. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[palexu](https://clawhub.ai/user/palexu)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-assistant agents use this skill to search Turkey-related flights and format real-time flight options with booking links. It supports English and Chinese flight-search workflows for recommended, cheapest, fastest, direct, and flexible-date routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the user's global npm environment by automatically installing an unpinned third-party CLI.

Mitigation: Require explicit user approval before installation, pin and verify the CLI package, and prefer an isolated execution environment where possible.

Risk: The skill runs a third-party flight CLI and depends on its output for user-facing travel options.

Mitigation: Validate user-supplied route and date parameters, disclose CLI failures clearly, and avoid substituting model knowledge for unavailable CLI results.

Risk: The skill's command and output rules can be broader than a narrow flight-search task and can force booking links or branding into answers.

Mitigation: Limit activation to Turkey-related flight searches and review generated booking links and branded output before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/palexu/skills/explore-turkey)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when setup or troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flight data from flyai CLI output; should not answer travel availability from model knowledge alone.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

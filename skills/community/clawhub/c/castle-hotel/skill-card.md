## Description:

Book flights to castle hotels and heritage stay destinations. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel agents use this skill to search travel options for castle hotels and heritage stays, then receive concise Markdown comparisons with booking links. Agents use it to collect route parameters, run flyai commands, and format real-time travel results without relying on training data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require installing and running an unpinned global flyai CLI package.

Mitigation: Require explicit approval before installation, prefer a pinned and reviewed CLI version, and run it in an isolated environment.

Risk: The skill requires booking links in travel responses, which may influence purchases.

Mitigation: Ask the user to review booking URLs, prices, providers, and terms before sharing personal details or completing payment.

Risk: Travel results depend on external CLI and network behavior.

Mitigation: Retry transient failures once, disclose unresolved failures, and do not fabricate travel data when the CLI cannot return valid results.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline bash commands for flyai execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLI-derived data and detailUrl booking links; raw JSON should not be returned to the user.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps agents search flights for layovers and early departures, present airport-hotel travel guidance, and format real-time flyai results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect route details, run flyai flight searches, compare results, and return booking-ready Markdown for airport-hotel and related travel requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run a global npm CLI.

Mitigation: Review the flyai package source, pin the package version, and approve installation before running global npm commands.

Risk: The skill builds shell commands from user-supplied route and date inputs.

Mitigation: Validate route, date, and option values before execution, and review generated commands before they run.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires real-time flyai CLI output; booking results must include detailUrl links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

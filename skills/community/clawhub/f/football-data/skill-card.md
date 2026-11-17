## Description:

Football Data helps agents retrieve football/soccer standings, schedules, match stats, expected goals, transfers, player profiles, and related league information across 13 competitions without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonelli182](https://clawhub.ai/user/antonelli182)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and sports analysts use this skill to answer football/soccer questions about league tables, fixtures, match reports, team form, player profiles, transfers, injuries, and expected-goals context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may execute unpinned package code, including code from a mutable GitHub fallback.

Mitigation: Install in an isolated virtual environment, prefer a pinned and reviewed PyPI release, and avoid the GitHub fallback unless it is pinned to a trusted commit.

Risk: The environment running the installed CLI could expose unnecessary credentials or sensitive files.

Mitigation: Run the skill with least-privilege filesystem and credential access, and do not provide secrets that are not required for football data lookups.

## Reference(s):

- [Football Data - Valid Commands & Common Mistakes](references/commands.md)
- [Football Data - Data Coverage by League](references/data-coverage.md)
- [Football Data - JSON Schemas](references/schemas.md)
- [Machina Sports](https://machina.gg)
- [Transfermarkt](https://www.transfermarkt.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, JSON examples, and football data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required. Output quality and availability depend on the covered league, command, and upstream sports data availability.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

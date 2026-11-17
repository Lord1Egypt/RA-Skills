## Description:

Book evening flights for after-work departure and dusk travel, with related travel booking support powered by Fliggy through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travel users and agent operators use this skill to collect route parameters, run live flyai CLI searches for evening, cheapest, fastest, or direct flights, and return concise booking results with required links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run a third-party flight CLI globally.

Mitigation: Review before installing, prefer manual pinned local or sandboxed installation, and require confirmation before any install or live search.

Risk: The skill sends user travel searches to a third-party CLI.

Mitigation: Use only when users are comfortable sharing route, date, and preference details with that CLI, and avoid unusual free-form route text until command argument handling is explicit.

Risk: The skill can execute user-derived shell commands without detailed safety boundaries.

Mitigation: Collect only the required parameters, map them to documented flags, and confirm live searches before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/evening-flight)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown flight summaries and comparison tables with inline booking links, based on flyai CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires detailUrl booking links in every result and should not expose raw JSON.]

## Skill Version(s):

3.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

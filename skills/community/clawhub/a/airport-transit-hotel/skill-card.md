## Description:

Find hotels near airports for layovers, early morning flights, or late-night arrivals, sorted by distance to terminal with shuttle information and booking links powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to find airport-area hotels for layovers, late arrivals, and early departures using live flyai CLI results. It helps compare nearby hotel options and present booking links without relying on model training data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned global third-party npm CLI.

Mitigation: Review the CLI package before installation, pin an approved version where possible, and run it in a constrained environment.

Risk: Travel searches may be sent to the flyai/Fliggy service and booking links may direct users to an external provider.

Mitigation: Use the skill only when that provider dependency is acceptable, and review generated booking links before acting on them.

Risk: The artifact describes local logging of raw travel queries and command execution details.

Mitigation: Disable, constrain, or regularly clear local execution logs when queries may contain sensitive travel details.

## Reference(s):

- [Airport Transit Hotel README](README.md)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)
- [Parent flyai Skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/airport-transit-hotel)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be based on live flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter describes 2.0.0 behavior)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

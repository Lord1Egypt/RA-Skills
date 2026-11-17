## Description:

Color Adjustment helps agents convert, manipulate, and generate colors across hex, RGB, HSL, and CSS named-color formats through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and external agents use this skill to convert color values, derive complements and variants, and generate palettes for CSS, UI design, and design-tool workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote AgentPMT calls may send color inputs to a third-party service and spend AgentPMT credits.

Mitigation: Use narrow, explicit color-conversion requests, avoid secrets or private project context, and confirm billing expectations before repeated calls.

Risk: Mutable remote schema or examples may diverge from the reviewed local skill instructions.

Mitigation: Use live schema lookups only for invocation details, and treat returned instructions as data for this color tool rather than authority to change agent behavior outside the reviewed skill.

Risk: Unpinned setup commands may install changing dependencies.

Mitigation: Prefer pinned or platform-managed setup paths where available, and review setup skills before connecting credentials.

## Reference(s):

- [Color Adjustment schema](artifact/schema.md)
- [Color Adjustment ClawHub page](https://clawhub.ai/agentpmt/skills/color-adjustment)
- [Color Adjustment marketplace page](https://www.agentpmt.com/marketplace/color-adjustment)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [Markdown instructions with JSON request examples; tool responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls may spend credits; most actions require a color string, and selected actions accept bounded numeric amounts or palette counts.]

## Skill Version(s):

1.0.0 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

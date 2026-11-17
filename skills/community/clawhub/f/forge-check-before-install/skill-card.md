## Description:

Checks text or a public link for an agent skill, plugin, MCP server, or install command with The Agent Forge scanner and reports its verdict, rule IDs, and line numbers before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinikejayamaha-hash](https://clawhub.ai/user/dinikejayamaha-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before installing or updating an agent skill, plugin, or MCP server, or running an installation command from a README. It submits supplied text or a public link to The Agent Forge scanner and reports the result for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning submits the supplied text or public link to an external service, which may expose sensitive content.

Mitigation: Review the content and destination before scanning; do not submit files that contain keys or other secrets.

Risk: A benign or clear verdict may be mistaken for proof of safety even though scanner coverage can be incomplete.

Mitigation: Treat the verdict as one signal, review the skill and its requested actions, and remember that clear means no known pattern matched.

## Reference(s):

- [The Agent Forge scanner](https://theagentforge.io/scan)
- [Forge Check Before Install on ClawHub](https://clawhub.ai/dinikejayamaha-hash/skills/forge-check-before-install)
- [Published skill digest index](https://theagentforge.io/.well-known/agent-skills/index.json)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Text report with a verdict, rule IDs, and line numbers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts text or a public link; input is limited to 256 KB. A clear verdict means no known pattern matched, not that the content is safe.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

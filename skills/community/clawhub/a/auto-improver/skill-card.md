## Description:

Auto-improving AI agent that learns from every execution, extracts patterns, and continuously optimizes itself. 17-minute autonomous loop with confidence scoring and skill evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to run an autonomous improvement loop that observes executions, detects reusable patterns, extracts improvement candidates, and aggregates them into skills, commands, or agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file write and command-execution capabilities.

Mitigation: Install and run it only in a tightly sandboxed environment with minimal filesystem and shell permissions.

Risk: The advertised learning and self-improvement behavior is not implemented in the package.

Mitigation: Validate the package behavior against the release claims before relying on it for workflow improvement.

Risk: The implementation is designed to run continuously.

Mitigation: Use explicit operator controls, monitoring, and time limits before allowing unattended execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/auto-improver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe or execute a continuous local improvement loop; review behavior and permissions before deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

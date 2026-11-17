## Description:

Search coastal, seaside city, and beach-town flights with booking links, plus related travel tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel agents use this skill to search real-time coastal flight options, compare recommended, budget, and direct routes, and present Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global flyai CLI before use.

Mitigation: Review the CLI package and require explicit user approval before any global npm install.

Risk: The skill depends on shell commands built from travel search parameters.

Mitigation: Validate origin, destination, dates, and supported flags before execution, and avoid passing untrusted free-form text into shell commands.

Risk: The skill may persist raw travel queries to a local execution log.

Mitigation: Do not enter sensitive personal, payment, passport, visa, or account details unless logging is removed or clearly controlled.

## Reference(s):

- [Parameter and output templates](references/templates.md)
- [Coastal flight playbooks](references/playbooks.md)
- [Fallback handling](references/fallbacks.md)
- [Execution log runbook](references/runbook.md)
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/coastal-flight)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be based on flyai CLI output and include booking links when flight results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

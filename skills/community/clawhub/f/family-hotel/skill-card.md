## Description:

Finds family-friendly hotels with multi-bed rooms, kid-friendly amenities, nearby playgrounds, and family-oriented services using flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search for family-oriented hotel options, compare real-time travel results, and receive booking links. Agents use it to collect required destination and date parameters, run flyai CLI hotel searches, and return concise Markdown recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run an unpinned global third-party travel CLI.

Mitigation: Review and approve the CLI package and version before installation, pin it in managed environments, and run commands in a sandboxed shell.

Risk: The runbook describes persisting raw travel requests that may include personal travel details, children's information, budgets, or dates.

Mitigation: Disable or remove execution-log persistence before handling sensitive travel queries and avoid storing raw personal details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/family-hotel)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with booking links and inline shell commands when setup or recovery is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel recommendations must be based on flyai CLI output and include detailUrl booking links.]

## Skill Version(s):

v3.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

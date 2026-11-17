## Description:

FOSSIL provides semantic failure memory for AI agents, helping them search past reasoning failures before acting and record new failures with resolutions afterward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyrtl](https://clawhub.ai/user/heyrtl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Fossil to add failure-memory workflows to OpenClaw agents, searching for similar past failures before risky steps and recording new failures and resolutions afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote hosted memory service may receive task descriptions or failure summaries that include sensitive data.

Mitigation: Sanitize descriptions and avoid recording secrets, personal data, customer details, raw prompts, filenames, or regulated information.

Risk: The suggested AGENTS.md persistence block can cause future sessions to use remote failure memory by default.

Mitigation: Add persistent guidance only when that behavior is intentional and scope it to appropriate projects.

Risk: An unpinned npx package install can change behavior across installs.

Mitigation: Pin the @openfossil/mcp package version before production use.

## Reference(s):

- [FOSSIL homepage](https://github.com/heyrtl/fossil)
- [FOSSIL docs](https://github.com/heyrtl/fossil/tree/main/docs)
- [FOSSIL protocol](https://github.com/heyrtl/fossil/blob/main/FOSSIL.md)
- [FOSSIL REST API health endpoint](https://fossil-api.hello-76a.workers.dev/health)
- [ClawHub release page](https://clawhub.ai/heyrtl/skills/fossil)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP setup guidance and suggested failure-memory usage patterns.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Analyze Claude Code token usage by parsing local session logs to show token allocation, project costs, and burn-rate drivers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[singggggyee](https://clawhub.ai/user/singggggyee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Claude Code token usage, identify high-cost projects or sessions, and choose narrower reports such as recent-day or per-session breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer can read all matching Claude Code session logs for the account, which may include sensitive conversation and project data.

Mitigation: Use narrow date ranges or session-specific commands, and review any JSON or per-turn output before sharing it.

Risk: The skill depends on an external CLI that is not included or version-pinned by the skill package.

Mitigation: Verify the CLI source and installed version before use.

## Reference(s):

- [Claude Usage Analyzer on ClawHub](https://clawhub.ai/singggggyee/skills/claude-usage-analyzer)
- [Claude Usage Analyzer CLI Repository](https://github.com/SingggggYee/claude-usage-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize local Claude Code session logs and suggest narrower date ranges or session-specific commands.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

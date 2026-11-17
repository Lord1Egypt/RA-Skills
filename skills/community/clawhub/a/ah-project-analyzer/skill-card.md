## Description:

Project Analyzer helps agents inspect existing codebases, map architecture, assess code quality, and produce prioritized improvement reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform structured discovery of a repository, summarize its technology stack and architecture, assess maintainability and security patterns, and create an actionable project analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to inspect repository files, which may expose private source code, configuration details, or documentation to the active agent session.

Mitigation: Use it only in repositories the user is comfortable letting an agent inspect, and avoid running it on projects containing secrets or sensitive data that should not be reviewed in-session.

Risk: The skill suggests shell usage for discovery and counting commands.

Mitigation: Keep command usage read-only and limited to discovery, search, and counting actions consistent with the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-project-analyzer)
- [Publisher profile](https://clawhub.ai/user/mtsatryan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with structured findings and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file references, command suggestions, architecture summaries, and suggested follow-up agents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

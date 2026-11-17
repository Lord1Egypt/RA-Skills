## Description:

Checks GitHub release and changelog information for Claude Code, OpenClaw, and NousResearch Hermes Agent to report latest versions and recent changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzx0](https://clawhub.ai/user/jzx0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for latest version summaries, date-bounded changelog entries, and multi-tool status comparisons for supported AI agent tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic requests about updates or latest versions may activate this skill even when multiple tools could match.

Mitigation: Ask the user to confirm the intended tool when the request is ambiguous.

Risk: Version summaries may be incomplete if a GitHub release page is unavailable or too large to fetch fully.

Mitigation: Report inaccessible sources clearly and supplement releases with the configured changelog when available.

## Reference(s):

- [Claude Code GitHub Releases](https://github.com/anthropics/claude-code/releases)
- [OpenClaw GitHub Releases](https://github.com/openclaw/openclaw/releases)
- [Hermes Agent GitHub Releases](https://github.com/nousresearch/hermes-agent/releases)
- [OpenClaw CHANGELOG](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown tables and bullet summaries with links and optional upgrade commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries depend on public GitHub release and changelog availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

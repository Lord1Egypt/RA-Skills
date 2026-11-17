## Description:

Analyzes local Claude Code, Codex, and Kimi Code session data so an agent can summarize activity, tool use, projects, timelines, and friction points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanktechnology](https://clawhub.ai/user/tanktechnology)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local AI coding assistant histories, compare Claude Code, Codex, and Kimi Code activity, and produce observations about projects, tool patterns, and recent workflow changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Claude Code, Codex, and Kimi Code session histories that may include sensitive file paths, commands, project names, and workflow details.

Mitigation: Run it only on trusted local machines, prefer terminal summaries or the HTML report with --no-open for sensitive logs, and do not share generated reports.

Risk: The authoritative security summary says the HTML report handles sensitive local data in ways that need review before installation.

Mitigation: Review the generated report behavior before using the skill on sensitive work logs, and address the CDN dependency and unescaped report fields noted in the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanktechnology/skills/ai-session-analysis)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text analysis, with optional self-contained HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize sensitive local session history; HTML reports should remain local.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

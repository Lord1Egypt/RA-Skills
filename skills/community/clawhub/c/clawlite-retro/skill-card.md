## Description:

ClawLite Retro helps engineering teams generate periodic retrospectives from Git history, quality metrics, contributor activity, and backlog signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill to produce 24-hour, 7-day, 14-day, or 30-day engineering retrospectives from a repository's Git activity. It summarizes commits, contributors, testing activity, hotspots, work sessions, backlog health, and concrete follow-up focus areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches from the repository origin and reads local Git author names, emails, commit history, file-change summaries, and TODOS.md.

Mitigation: Use it only in repositories where retrospective analysis is expected and where fetching origin and reviewing local repository metadata are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/clawlite-retro)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown retrospective with tables, histograms, contributor analysis, and recommended next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports /retro, /retro 24h, /retro 14d, and /retro 30d time windows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

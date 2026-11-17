## Description:

Agent Daily Planner helps agents organize daily work, carry context across sessions, track blockers, and record shipped work in persistent local planning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpunter](https://clawhub.ai/user/gpunter)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create daily plans, carry unfinished work forward, log shipped outcomes, track blockers, and summarize weekly progress across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or modifies local planning files under memory/.

Mitigation: Review proposed planning changes before relying on them, especially when commands update today's priorities or carry forward unfinished work.

Risk: /plan priorities overwrites the current day's Priority Tasks section.

Mitigation: Check the current daily plan before replacing priorities, and keep important context in Notes or project tracking files.

## Reference(s):

- [Agent Daily Planner on ClawHub](https://clawhub.ai/gpunter/skills/agent-daily-planner)
- [gpunter ClawHub profile](https://clawhub.ai/user/gpunter)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown planning notes and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under memory/ for daily logs and weekly summaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

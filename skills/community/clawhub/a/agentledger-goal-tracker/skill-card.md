## Description:

OKR-style goal tracking for solopreneurs with quarterly goals, weekly check-ins, progress scoring, and drift detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

External users and developers use this skill to have an agent create and maintain local goal-tracking files, run weekly check-ins, score progress against key results, and prepare quarter-end retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to update local goal, retrospective, archive, and post-mortem files during check-ins.

Mitigation: Use explicit check-in prompts and review changes to goals/GOALS.md, retrospectives, and archives before relying on them.

Risk: Optional heartbeat or cron examples can create scheduled reminders in a configured chat.

Mitigation: Add the heartbeat or cron examples only when scheduled reminders are desired and the target chat is configured correctly.

## Reference(s):

- [Advanced Patterns](references/advanced-patterns.md)
- [Goal Tracker on ClawHub](https://clawhub.ai/clawdssen/skills/agentledger-goal-tracker)
- [Publisher Profile](https://clawhub.ai/user/clawdssen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and goal-tracking templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local goal, retrospective, archive, and post-mortem files when used by an agent.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

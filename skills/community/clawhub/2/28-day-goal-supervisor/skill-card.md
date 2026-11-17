## Description:

GrowthLoop helps users turn habit goals into practical 28-day plans, track daily check-ins, adjust difficulty, view progress, and receive reminders for up to five habits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chestnuuutli](https://clawhub.ai/user/chestnuuutli)

### License/Terms of Use:


## Use Case:

External users use this agent to create habit goals, refine them into feasible plans, record daily progress, and review summaries or visualizations. It is suited to personal productivity workflows where local tracking and coaching-style reminders are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores habit goals, notes, reminders, and some coaching conversation history locally in plaintext.

Mitigation: Use a private data directory with restrictive filesystem permissions and avoid entering sensitive health, work, or personal details.

Risk: The skill automatically checks and may update reminder state across conversations.

Mitigation: Review or disable heartbeat reminder behavior if unrelated conversations should not access or mutate habit reminder state.

Risk: External or scheduled reminder paths can expose data or trigger habit checks outside the current chat context.

Mitigation: Enable cron, launchd, GitHub Actions, or endpoint-based reminders only after reviewing the schedule, data directory, and endpoint exposure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chestnuuutli/skills/28-day-goal-supervisor)
- [Coaching Style Guide](artifact/references/coaching_style.md)
- [Edge Case Handling Guide](artifact/references/edge_cases.md)
- [Plan Generation Rules](artifact/references/plan_generation_rules.md)
- [Goal Rationalization Guide](artifact/references/rationalization_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with optional CLI commands, JSON-backed records, text charts, and SVG progress visualizations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and stores habit data locally in plaintext unless the user configures a protected data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

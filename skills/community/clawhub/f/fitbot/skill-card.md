## Description:

Personal fitness coaching for training, workouts, programs, progression, and fitness accountability, including onboarding, custom program design, session coaching, and on-the-fly adaptation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conmeara](https://clawhub.ai/user/conmeara)

### License/Terms of Use:


## Use Case:

External users and personal coaching agents use Fitbot to gather fitness context, build custom training programs, coach sessions, maintain workout records, and adapt workouts around constraints, missed sessions, and pain without diagnosing medical conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores fitness, injury, schedule, and motivation details as plaintext workspace files.

Mitigation: Use it only in a private workspace and review, redact, or delete stored fitness files when they are no longer needed.

Risk: Reminder automation can persist after setup if cron or heartbeat entries are created.

Mitigation: Enable reminders only by explicit choice and confirm how to disable any cron or heartbeat entries before relying on them.

Risk: Fitness adaptations around pain can be mistaken for medical guidance.

Mitigation: Keep recommendations non-diagnostic, adapt training conservatively, and refer clinical symptoms or medical decisions to a qualified professional.

## Reference(s):

- [Fitbot Skill Page](https://clawhub.ai/conmeara/skills/fitbot)
- [Fitbot Onboarding](references/onboarding.md)
- [Program Design Guide](references/program-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown coaching responses with workspace Markdown files and occasional shell commands for setup or reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local fitness profile, program, and workout log files; may propose reminder automation when explicitly requested.]

## Skill Version(s):

0.1.1 (source: server release metadata, released 2026-02-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

ADHD Founder Planner helps users create ADHD-friendly daily and monthly plans with rapid logging, energy-based swim lanes, task migration, reflection, and dopamine rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jankutschera](https://clawhub.ai/user/jankutschera)

### License/Terms of Use:

MIT

## Use Case:

External users and productivity-focused agents use this skill to structure daily planning, task capture, task migration, and end-of-day reflection for ADHD-friendly founder workflows. It is suited to local planning assistance where flexible energy-based organization is preferred over rigid schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The planner stores task lists, reflections, wins, blockers, and energy notes in local Markdown files.

Mitigation: Avoid entering highly sensitive information unless local file storage and backups are acceptable for the user.

Risk: Relative time blocks may be insufficient for fixed commitments and appointments.

Mitigation: Use exact calendar entries and alarms for time-critical obligations.

Risk: Re-running the planning command can replace the current day's planning file.

Mitigation: Review the existing daily file or keep backups before rerunning a full planning session.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jankutschera/skills/adhd-founder-planner)
- [ADHD-founder.com](https://adhd-founder.com)
- [Founder Circle](https://adhd-founder.com/founder-circle)
- [Migration Reference](references/migration.md)
- [Swim Lanes Reference](references/swim-lanes.md)
- [Rapid Logging Symbols](references/symbols.md)
- [Time-Blindness Planning](references/time-blindness.md)
- [ADHD Body Doubling](https://github.com/jankutschera/adhd-body-doubling)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown planner entries with concise command and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local daily and monthly planning Markdown files when the shell helper is used.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

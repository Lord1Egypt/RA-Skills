## Description:

Your personal desk health coach with automated break reminders that generates platform-specific scripts for 20-20-20 eye care, lower back exercises, RSI prevention, ergonomic guidance, and customizable notification systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akhmittra](https://clawhub.ai/user/akhmittra)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, remote workers, students, gamers, and desk-based teams use this skill to get preventive desk-health exercise guidance and generate local reminder scripts for eye breaks, stretches, RSI prevention, and ergonomic routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated bash or PowerShell reminder scripts may be executed locally and may run continuously or at startup.

Mitigation: Review each generated script before use, run it as a normal user from a dedicated directory, and enable startup only after explicitly confirming the behavior.

Risk: Shell or PowerShell profile autostart can make generated reminders persistent in ways users may overlook.

Mitigation: Prefer clear start and stop commands, avoid profile-based autostart, and document uninstall or disable steps before enabling persistence.

Risk: The skill provides preventive wellness and ergonomic guidance, not medical diagnosis or treatment.

Mitigation: Use it for prevention and mild discomfort only, and seek healthcare advice for severe, persistent, radiating, or worsening symptoms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akhmittra/skills/ergocare-coach)
- [Publisher profile](https://clawhub.ai/user/akhmittra)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash or PowerShell code blocks and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable local reminder scripts, desktop notification setup, schedule configuration, and preventive ergonomic guidance.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

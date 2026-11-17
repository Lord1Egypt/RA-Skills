## Description:

Safety Check-In Reminder sends daily Feishu check-in prompts and escalates to an emergency contact after seven missed days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayhe](https://clawhub.ai/user/jayhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users or operators use this skill to configure daily safety check-ins through a Feishu group and emergency-contact escalation after prolonged inactivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an emergency phone number and Feishu chat ID in local project files.

Mitigation: Confirm the user and emergency contact consent to storing this data, restrict file access, and delete stored configuration when the workflow is no longer needed.

Risk: The skill creates recurring automation that may continue after the user stops intending to use it.

Mitigation: Provide and verify a way to list, disable, delete, and expire scheduled reminder and check tasks.

Risk: The skill may contact a third party after missed check-ins.

Mitigation: Verify the Feishu destination and emergency phone number before activation, and confirm escalation behavior with the emergency contact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayhe/skills/dead-or-alive)
- [Publisher profile](https://clawhub.ai/user/jayhe)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Files, Shell commands, API Calls]

**Output Format:** [Markdown guidance with configuration updates, local log files, scheduled automation, Feishu reminders, and emergency-contact notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local configuration and log files for check-ins and alerts.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

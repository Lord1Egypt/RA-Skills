## Description:

Calendar Manager helps users manage schedules, reminders, holidays, anniversaries, countdowns, and time statistics through Chinese-language calendar interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to add, view, complete, and delete calendar events, query holidays, manage anniversaries, and generate countdown or schedule-summary responses in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar entries are stored locally and may include sensitive schedule details.

Mitigation: Avoid storing highly sensitive details in shared workspaces and restrict access to the local calendar data files.

Risk: Deletion commands can permanently remove stored events when a matching event ID is provided.

Mitigation: Review delete or cancel requests before execution and keep a backup for important schedule data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/cp3d1455926-svg-calendar-manager)
- [Publisher profile](https://clawhub.ai/user/cp3d1455926-svg)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Chinese-language text and Markdown responses, with local JSON event records when schedule data is stored]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores calendar data locally in JSON files; no network output is indicated by the security evidence.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

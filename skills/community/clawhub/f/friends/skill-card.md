## Description:

Build a personal friendship system with interaction tracking, relationship health, and proactive maintenance reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to maintain a private friendship journal, track meaningful interactions and life events, and receive prompts for check-ins, reconnection, and conflict repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages long-term plaintext records about identifiable friends, including sensitive life events and relationship context.

Mitigation: Use it only for a private local friendship journal, avoid recording highly sensitive details unless deliberate, restrict folder permissions, and review or delete old records periodically.

Risk: Friendship notes may include information about people who have not consented to being tracked.

Mitigation: Keep entries minimal, factual, and respectful; avoid unnecessary health, mental-health, children, grief, conflict, or location details.

Risk: Sync or backup tools could expose the ~/friends/ folder beyond the local machine.

Mitigation: Exclude the folder from sync and backups unless the user has intentionally chosen protected storage.

## Reference(s):

- [Friends Skill Page](https://clawhub.ai/ivangdavila/skills/friends)
- [Making New Friends](artifact/making.md)
- [Deepening Friendships](artifact/deepening.md)
- [Friendship Conflicts](artifact/conflicts.md)
- [Reconnecting with Lost Friends](artifact/reconnecting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Configuration instructions]

**Output Format:** [Markdown guidance and Markdown friendship records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local plaintext files under ~/friends/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

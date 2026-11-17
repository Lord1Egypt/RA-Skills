## Description:

A Chinese-language local reminder-note skill for storing reminders, countdown labels, and anniversaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07)

### License/Terms of Use:

MIT

## Use Case:

External users can use this skill to capture simple Chinese-language reminder, countdown, and anniversary notes and view the saved list later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered reminders, countdowns, and anniversaries are stored as plaintext JSON files in the skill directory.

Mitigation: Avoid storing sensitive personal details unless plaintext local storage is acceptable for the deployment.

Risk: The skill presents reminder and countdown features, but the security assessment says it is not a real notification or countdown engine.

Mitigation: Use it as a local reminder-note list and do not rely on it for time-critical notifications.

Risk: The security guidance notes no built-in delete or export command.

Mitigation: Plan an external data-management process before using it for reminders that may need retention, removal, or transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/skills/daily-reminder)
- [ClawHub publisher profile](https://clawhub.ai/user/huangjingzhi07)

## Skill Output:

**Output Type(s):** [text, JSON files]

**Output Format:** [Chinese-language text responses with locally stored JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered reminders, countdowns, and anniversaries in local JSON files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

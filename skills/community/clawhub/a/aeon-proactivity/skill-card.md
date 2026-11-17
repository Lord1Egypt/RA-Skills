## Description:

Aeon Proactivity helps AEON agents learn from user feedback, record lessons, remember preferences and reminders, and improve future interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an AEON agent adapt from corrections, retain local cross-session notes, remember preferences and reminders, suggest useful skills or automations, and ask for clarification before risky actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad conversation history, work habits, preferences, reminders, and configuration changes.

Mitigation: Install only when local cross-session memory is desired, require confirmation before storing long-term learnings, and review or delete memory files regularly.

Risk: Persistent memory may capture secrets or personal data if used in sensitive conversations.

Mitigation: Avoid using the skill around secrets or personal data and do not store passwords, keys, full command outputs, or other sensitive details.

Risk: The security review notes unclear opt-in, retention, and redaction controls.

Mitigation: Use explicit user consent for memory behavior, keep retention limited, and periodically remove outdated or conflicting entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gu2003li/skills/aeon-proactivity)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with plain-language responses and suggested shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local markdown memory files for lessons, reminders, preferences, success patterns, and configuration history.]

## Skill Version(s):

2.7.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

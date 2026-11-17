## Description:

Create Feishu (Lark) video meetings via the Calendar API for instant, scheduled, or recurring events with invitee resolution, automatic VC links, recurrence support, and calendar integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicaldd](https://clawhub.ai/user/magicaldd)

### License/Terms of Use:


## Use Case:

External users, developers, and operations teams use this skill to create Feishu or Lark video meetings from an agent workflow, including scheduled or recurring meetings with attendees added to Feishu calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted meeting titles, recurrence rules, or start times may be interpreted by embedded Python in the shell script.

Mitigation: Pass user-controlled values to Python via arguments or stdin, validate them before use, and avoid using the skill with untrusted meeting input until this is fixed.

Risk: The skill creates calendar events and sends invitee phone or email data to Feishu using broad calendar-writing authority.

Mitigation: Use a least-privilege Feishu app, run under an unprivileged account, and require explicit user confirmation before creating events or submitting invitee data.

## Reference(s):

- [Feishu bot capability documentation](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-enable-bot-ability)
- [Feishu calendar list API](https://open.feishu.cn/open-apis/calendar/v4/calendars)
- [ClawHub skill page](https://clawhub.ai/magicaldd/skills/feishu-meeting)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; command execution returns text meeting details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command output includes meeting status, topic, Feishu meeting link, attendee names, recurrence details when present, and unresolved invitee notices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Natural language reminders that create actual Apple Reminders.app entries (macOS-native).

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

External users and agents use this skill on macOS to create, list, complete, edit, reschedule, and delete Apple Reminders entries from natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete reminders by ID without an interactive prompt.

Mitigation: Review deletion requests and reminder IDs carefully before allowing delete actions.

Risk: The skill can edit, reschedule, or complete existing reminders.

Mitigation: Confirm the target reminder and requested change before allowing actions that modify existing reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plgonzalezrx8/skills/apple-remind-me)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for macOS and require remindctl and BSD date.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

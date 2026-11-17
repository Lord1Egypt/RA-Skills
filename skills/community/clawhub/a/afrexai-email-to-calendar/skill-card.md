## Description:

Extract calendar events, deadlines, action items, and follow-ups from emails for review and confirmed calendar creation across common calendar providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to identify events, deadlines, travel logistics, reminders, and action items in email or inbox text, then review structured results before calendar creation or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to read email or inbox content, which can expose sensitive message data.

Mitigation: Use the skill only with explicit mailbox permissions and limit processing to emails or searches the user has approved.

Risk: Calendar create, update, or delete actions can change a user's schedule if automated incorrectly.

Mitigation: Require per-event user confirmation for every calendar change and avoid auto-create patterns.

Risk: Local commands such as shell or AppleScript examples may be less controlled than structured integrations.

Mitigation: Prefer structured calendar APIs or ICS output over raw shell or AppleScript commands when available.

Risk: Tracking logs may retain email subjects, message IDs, or calendar event IDs.

Mitigation: Disable or minimize persistent logs that store email and calendar identifiers unless the user explicitly accepts that retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-email-to-calendar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured YAML, JSON, shell command, and ICS examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents extracted calendar items for user confirmation; may output provider-specific creation commands, API guidance, or ICS content.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

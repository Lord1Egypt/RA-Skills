## Description: <br>
Extracts calendar events, deadlines, action items, and follow-ups from emails for review and calendar creation across common calendar providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and employees use this skill to have an agent parse forwarded, pasted, or inbox emails for calendar events, deadlines, action items, travel logistics, and reminders, then present entries for confirmation before creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read sensitive email content while extracting events and logistics. <br>
Mitigation: Limit scans to selected messages or narrow inbox windows and avoid broad mailbox access unless necessary. <br>
Risk: Extracted dates, timezones, titles, reminders, or recurrence rules may be incorrect or incomplete. <br>
Mitigation: Review each proposed calendar entry, especially medium- and low-confidence items, before allowing creation. <br>
Risk: Calendar creation through raw shell commands can be harder to audit than structured integrations. <br>
Mitigation: Prefer structured calendar APIs or ICS export when available, and inspect command parameters before execution. <br>
Risk: Email-calendar memory files can retain sensitive subjects, travel details, or event identifiers. <br>
Mitigation: Periodically clear local email-calendar preference and tracking files that contain sensitive details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-email-to-calendar) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured event fields, calendar command examples, configuration snippets, and ICS snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar items are presented for user confirmation before creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

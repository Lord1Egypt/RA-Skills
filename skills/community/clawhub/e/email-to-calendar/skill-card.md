## Description: <br>
Extract calendar events from emails and create calendar entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonimelisma](https://clawhub.ai/user/tonimelisma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and external users use this skill to extract events, deadlines, and action items from emails, review them, and create or update calendar entries with duplicate detection and undo support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read email bodies, modify inbox state, and create or update calendar events. <br>
Mitigation: Install only with the intended email and calendar access; prefer forwarded-email mode over direct inbox scanning and review attendee and deadline-notification settings before use. <br>
Risk: Automatic mailbox changes and persistent local logging can affect inbox state and retain activity history. <br>
Mitigation: Disable mark-read and archive behavior until tested, and review local activity and extraction storage settings for the deployment environment. <br>
Risk: Evidence security guidance identifies a shell=True validation path as a bug for sensitive environments. <br>
Mitigation: Fix or avoid that path before using the skill in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonimelisma/email-to-calendar) <br>
- [Setup Guide](SETUP.md) <br>
- [CLI Reference](references/gog-commands.md) <br>
- [Extraction Patterns](references/extraction-patterns.md) <br>
- [Workflow Example](references/workflow-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update email and calendar state through wrapper scripts after user confirmation.] <br>

## Skill Version(s): <br>
1.13.1 (source: frontmatter, package.json, CHANGELOG, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Turn emails into Google Calendar events by reading Gmail messages, extracting meetings, appointments, RSVPs, and deadlines, and creating or updating Google Calendar entries after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonimelisma](https://clawhub.ai/user/tonimelisma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn email-based meetings, appointments, RSVP requests, and deadlines into reviewed Google Calendar events. It is useful for inbox-to-calendar workflows where the agent should present extracted events, check for duplicates, and apply confirmed changes through local wrapper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change Gmail state and persistent workspace behavior after setup. <br>
Mitigation: Review setup defaults before installing, and turn off mark_read, archive, and auto_dispose_calendar_replies for preview-only behavior. <br>
Risk: Local logs and state may contain email IDs, subjects, event titles, and calendar metadata. <br>
Mitigation: Keep the workspace and data directory access controlled, and review local log retention before using the skill with sensitive mailboxes. <br>
Risk: Persistent HEARTBEAT.md changes can affect ongoing behavior. <br>
Mitigation: Inspect any HEARTBEAT.md changes before allowing them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tonimelisma/skills/email-to-calendar) <br>
- [Setup guide](SETUP.md) <br>
- [Extraction patterns](references/extraction-patterns.md) <br>
- [gog command reference](references/gog-commands.md) <br>
- [Workflow example](references/workflow-example.md) <br>
- [gog CLI](https://github.com/tonimelisma/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured event details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewed event proposals, confirmation prompts, local wrapper-script commands, setup guidance, and undo or follow-up instructions.] <br>

## Skill Version(s): <br>
1.13.3 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

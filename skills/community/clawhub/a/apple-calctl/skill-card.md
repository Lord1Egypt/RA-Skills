## Description: <br>
Command-line tool for macOS Sonoma that manages Apple Calendar events using EventKit with create, list, edit, and delete capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianteohx](https://clawhub.ai/user/christianteohx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to install and operate calctl for creating, listing, editing, and deleting Apple Calendar events from the terminal, including recurring events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool requires macOS Calendar permission and can access calendar event data. <br>
Mitigation: Grant Calendar permission knowingly and use the access-status command before relying on calendar operations. <br>
Risk: Calendar edit and delete commands can modify or remove user events. <br>
Mitigation: Confirm add, edit, and delete actions before running generated commands. <br>
Risk: Using attendee output can expose attendee names, email addresses, and response statuses. <br>
Mitigation: Avoid the attendee flag unless that information is needed for the task. <br>
Risk: Installation depends on an external calctl package source. <br>
Mitigation: Install only when the referenced package source is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/christianteohx/apple-calctl) <br>
- [calctl project homepage listed by the skill](https://github.com/christianteohx/calctl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include plain text or JSON command output when calctl is run with supported output options.] <br>

## Skill Version(s): <br>
1.2.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

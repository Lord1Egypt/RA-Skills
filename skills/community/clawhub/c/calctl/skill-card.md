## Description:

Manage Apple Calendar events via icalBuddy + AppleScript CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainbat](https://clawhub.ai/user/rainbat)

### License/Terms of Use:


## Use Case:

Developers and command-line users use this skill to manage local Apple Calendar events: list calendars, show events, add events, and search upcoming events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event creation may target an unintended local calendar because the documented default calendar is Privat.

Mitigation: Confirm the target calendar before running calctl add, and pass --calendar with the intended local Apple Calendar name.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Apple Calendar access and icalBuddy for calendar reads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

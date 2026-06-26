## Description: <br>
Manage Apple Calendar events via AppleScript, with artifact-backed support for adding events using smart date parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoL0rd](https://clawhub.ai/user/CryptoL0rd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers on macOS use this skill to add Apple Calendar events with relative or explicit dates through OpenClaw-managed shell commands and AppleScript automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write events to a local Apple Calendar once macOS automation permission is granted. <br>
Mitigation: Review the calendar name, event title, dates, and times before executing generated commands, and grant Calendar automation permission only for trusted use. <br>
Risk: The artifact references an add_event.scpt implementation that is not included in the supplied artifact files. <br>
Mitigation: Inspect and verify any separately supplied add_event.scpt before using it with Calendar automation permissions. <br>


## Reference(s): <br>
- [Apple Calendar Manager on ClawHub](https://clawhub.ai/CryptoL0rd/apple-calendar-manager) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local macOS Calendar automation commands that require user-granted Calendar automation permission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

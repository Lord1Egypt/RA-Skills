## Description: <br>
iCloud Calendar skill via CalDAV (RFC 4791) - works on macOS/Linux, and Windows with env/keyring auth. Supports event CRUD, multi-calendar queries, managed attachments (RFC 8607), and free/busy lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xushen-ma](https://clawhub.ai/user/xushen-ma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and calendar automation users use this skill to let an agent list, create, update, and delete iCloud Calendar events, query multiple calendars, manage event attachments, and check availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify iCloud Calendar data. <br>
Mitigation: Install it only when that access is intended, and review create, update, delete, and attachment commands before execution. <br>
Risk: Calendar access depends on an Apple app-specific password or local credential store. <br>
Mitigation: Use an app-specific password and prefer keyring or macOS Keychain over storing APPLECAL_PASSWORD in a persistent shell profile. <br>
Risk: Attachment commands can upload local files into calendar events. <br>
Mitigation: Use APPLECAL_ATTACH_DIR to limit attachable files and rely on the skill's extension allowlist and sensitive path/name blocking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xushen-ma/apple-calendar-pro) <br>
- [Publisher profile](https://clawhub.ai/user/xushen-ma) <br>
- [Skill homepage](https://github.com/xushen-ma/apple-calendar-pro) <br>
- [Apple app-specific passwords](https://appleid.apple.com) <br>
- [iCloud CalDAV endpoint](https://caldav.icloud.com/.well-known/caldav) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the calendar CLI, with Markdown command examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, an iCloud account with Calendar enabled, and APPLECAL_PASSWORD or keyring/Keychain credential access.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

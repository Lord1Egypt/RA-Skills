## Description:

iCloud Calendar skill via CalDAV (RFC 4791) for event CRUD, multi-calendar queries, managed attachments (RFC 8607), and free/busy lookups across macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xushen-ma](https://clawhub.ai/user/xushen-ma)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to manage iCloud calendars through a Python CLI that lists, creates, updates, and deletes events, handles managed attachments, and checks availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Apple app-specific password to access iCloud calendars, and the security evidence reports a URL-validation weakness that could expose that credential.

Mitigation: Use a dedicated revocable app-specific password, prefer keyring or Keychain storage over shell profiles, and avoid broad or unattended use until URL validation is fixed.

Risk: Create, update, delete, and attachment commands can change real calendar data.

Mitigation: Review command arguments before execution, verify target calendars and event IDs with list or get commands first, and restrict use to calendars where changes are intended.

Risk: Attachment upload commands can send local files to calendar entries.

Mitigation: Use the built-in attachment extension allowlist and sensitive path blocking, and set APPLECAL_ATTACH_DIR to a narrow approved attachment directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xushen-ma/skills/apple-calendar-pro)
- [README](artifact/README.md)
- [Apple app-specific passwords](https://appleid.apple.com)
- [iCloud CalDAV well-known endpoint](https://caldav.icloud.com/.well-known/caldav)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, API calls]

**Output Format:** [JSON from Python CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or modify live iCloud calendar data and require APPLECAL_PASSWORD or a supported keyring.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Apple Cal Anywhere lets agents manage iCloud Calendar across macOS, Linux, and Windows via CalDAV, including event CRUD, multi-calendar queries, managed attachments, and free/busy lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xushen-ma](https://clawhub.ai/user/xushen-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect and manage Apple Calendar data, create, update, and delete events, upload managed attachments, and check availability through the bundled CalDAV CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify specified iCloud calendars using app-specific credentials.

Mitigation: Use an Apple app-specific password, prefer Python keyring or macOS Keychain storage, and install only when calendar read/write access is acceptable.

Risk: Persisting APPLECAL_PASSWORD in shell profiles or committed files can expose calendar credentials.

Mitigation: Avoid committing or broadly persisting APPLECAL_PASSWORD; use a credential store where possible and rotate the app-specific password if exposed.

Risk: Attachment commands upload local files to calendar events.

Mitigation: Use the built-in extension allowlist and sensitive-path blocking, and set APPLECAL_ATTACH_DIR to restrict uploads to an approved directory.

Risk: Runtime dependencies may change behavior if installed without version control.

Mitigation: Install dependencies in a locked virtual environment when deploying the skill in a managed environment.

## Reference(s):

- [Apple Cal Anywhere on ClawHub](https://clawhub.ai/xushen-ma/skills/apple-cal-anywhere)
- [Publisher profile](https://clawhub.ai/user/xushen-ma)
- [Project homepage](https://github.com/xushen-ma/apple-cal-anywhere)
- [Apple app-specific passwords](https://appleid.apple.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON responses from CLI commands, with Markdown setup and usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, an iCloud account with Calendar enabled, and APPLECAL_PASSWORD, Python keyring, or macOS Keychain authentication.]

## Skill Version(s):

1.3.1 (source: server release evidence, _meta.json, and scripts/applecal.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use local CLI to manage Apple, Google, iCloud, Outlook, CalDAV, and other calendars synced in macOS Calendar, without API keys or OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up, create, update, delete, and verify events in calendars already synced through macOS Calendar. It is intended for local-first calendar operations without provider OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change calendar events visible in macOS Calendar.

Mitigation: Keep destructive and bulk-edit confirmations enabled, require pre-read snapshots before writes, and verify changes with read-back.

Risk: Calendar writes can target the wrong event when duplicate titles, ambiguous dates, or recurrence rules are present.

Mitigation: Resolve events with at least two identifying fields, normalize timezone and date boundaries, and confirm recurrence and all-day semantics before writing.

Risk: Command path or macOS permission failures can produce incomplete reads or unsafe write assumptions.

Mitigation: Probe supported command paths before action, use read-only checks after permission changes, and stop when no safe fallback exists.

Risk: Local memory in ~/apple-calendar-macos/ may contain reusable calendar operation context.

Mitigation: Review stored files periodically, keep only required operational context, and confirm planned local file writes before saving.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/apple-calendar-macos)
- [Skill Homepage](https://clawic.com/skills/apple-calendar-macos)
- [Command Paths](artifact/command-paths.md)
- [Safety Checklist](artifact/safety-checklist.md)
- [Operation Patterns](artifact/operation-patterns.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bounded local calendar reads, explicit confirmations for writes, and post-write read-back verification.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

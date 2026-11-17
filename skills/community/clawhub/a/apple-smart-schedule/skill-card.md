## Description:

Converts natural-language schedule requests or ticket screenshots into macOS Calendar events and Reminders with configurable lead times that can sync through iCloud to Apple devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

External users and agents on macOS use this skill to turn travel, court, meeting, deadline, medical, and social scheduling requests into Apple Calendar events plus reminder entries. It is useful when a user wants an agent to create or update personal schedule records with event-specific advance reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar and Reminders automation can read or modify sensitive personal scheduling data that may sync through iCloud.

Mitigation: Install only when comfortable granting the invoking macOS app Calendar and Reminders access, and review created or updated entries before relying on them.

Risk: The security review reports unsafe handling of user-supplied schedule text in Calendar and Reminders automation scripts.

Mitigation: Review or fix AppleScript argument handling before using untrusted schedule text.

Risk: Broad calendar searches or fallback calendar/list selection can affect an unintended calendar or reminder list.

Mitigation: Verify configured calendar and reminder-list names, avoid ALL-calendar searches unless necessary, and ask the user to choose when duplicate candidates are found.

Risk: The optional remindctl dependency is installed from an external Homebrew tap.

Mitigation: Check the tap source and version before installing the optional dependency.

## Reference(s):

- [Lead-time Rules](references/lead-times.md)
- [Project Homepage](https://github.com/cat-xierluo/legal-skills)
- [ClawHub Skill Page](https://clawhub.ai/cat-xierluo/skills/apple-smart-schedule)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or concise status text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local macOS Calendar events and Reminders through scripts; requires macOS automation permissions.]

## Skill Version(s):

0.2.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

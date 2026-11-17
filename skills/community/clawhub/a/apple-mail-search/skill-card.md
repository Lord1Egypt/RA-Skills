## Description:

Fast Apple Mail search via SQLite on macOS. Search emails by subject, sender, date, attachments - results in ~50ms vs 8+ minutes with AppleScript. Use when asked to find, search, or list emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mneves75](https://clawhub.ai/user/mneves75)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, developers, and engineers use this skill to search local Apple Mail metadata quickly by subject, sender, recipient, date range, unread status, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal private local Apple Mail metadata such as subjects, addresses, dates, and attachment names.

Mitigation: Use narrow searches and small limits, and review results before sharing or exporting them.

Risk: CSV or JSON exports may persist sensitive email metadata outside Apple Mail.

Mitigation: Create exports only when needed, store them carefully, and delete exported files when they are no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mneves75/skills/apple-mail-search)
- [Project homepage](https://github.com/steipete/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide JSON or CSV export through the underlying mail-search command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

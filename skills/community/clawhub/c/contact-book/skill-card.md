## Description:

Store personal contacts with tags, search, and relationship tracking. Use when adding contacts, searching details, planning follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agents use this skill to maintain a local personal CRM, record contact details and relationship notes, plan follow-ups, track interactions, search prior activity, and export contact records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact details and relationship notes are stored and exported as unencrypted local plaintext.

Mitigation: Avoid highly sensitive entries, review local file permissions, and handle exported JSON, CSV, and TXT files as sensitive data.

Risk: Shared machines, backups, indexing tools, or downstream spreadsheet tools may expose exported contact data.

Mitigation: Use the skill on a trusted user account, limit access to ~/.local/share/contact-book, and delete or protect exports after use.

## Reference(s):

- [Contact Book ClawHub listing](https://clawhub.ai/ckchzh/skills/contact-book)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Plain text command output with local plaintext log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes per-command logs, a history log, and JSON, CSV, or TXT exports under ~/.local/share/contact-book.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

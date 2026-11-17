## Description:

Log and search local text entries from the command line. Use when adding quick notes, searching past entries, or exporting a simple activity log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use Bat to capture quick local notes, maintain a simple activity log, search prior entries, and export the log for backup or migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notes, search terms, and command history are stored locally in plain-text files under the Bat data directory.

Mitigation: Do not enter secrets or sensitive credentials, and set BAT_DIR to a controlled location with appropriate file permissions when needed.

Risk: The remove command logs a removal action but does not delete stored note content from the data log.

Mitigation: For true deletion, inspect and edit or delete the local data log directly according to the user's retention requirements.

## Reference(s):

- [Bat on ClawHub](https://clawhub.ai/xueyetianya/skills/bat)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text command output and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands write local plain-text data and history files under the Bat data directory.]

## Skill Version(s):

2.0.3 (source: server release metadata; artifact frontmatter says 2.0.2 and script says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

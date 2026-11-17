## Description:

Perform clipboard-tool operations from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to copy, paste, clear, and transform clipboard text from command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clipboard contents and copied text may be printed to terminal or agent logs.

Mitigation: Use only with non-sensitive clipboard content and avoid passwords, tokens, keys, or private files in logged sessions.

Risk: The skill can copy file contents to the clipboard.

Mitigation: Review file paths and contents before copying, especially when operating in shared or logged environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/clipboard-tool)
- [Publisher Profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from files, standard input, or the system clipboard depending on command options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

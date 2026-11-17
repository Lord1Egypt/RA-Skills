## Description:

Sorts files from compressed archives into target folders by matching filenames against configurable keyword rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zj-zc](https://clawhub.ai/user/zj-zc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview and execute archive extraction workflows that classify files into output directories based on reusable filename rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted archives or classification rules could write, move, or delete files outside the intended folder.

Mitigation: Install only after review or fixes, use trusted archives and trusted classification rules, and require explicit confirmation before execute or overwrite behavior.

Risk: The 7z/unrar command-line fallback may be inappropriate for sensitive or untrusted archives.

Mitigation: Avoid the command-line fallback for sensitive or untrusted archives and prefer reviewed dependencies or trusted archive inputs.

Risk: Passwords for protected archives may be exposed through process arguments.

Mitigation: Do not use password-protected archives when process arguments may be visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zj-zc/skills/compress-file-sorter)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell command examples and JSON rule configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces preview reports before confirmed move operations; output depends on archive contents and configured classification rules.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

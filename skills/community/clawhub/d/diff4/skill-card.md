## Description:

Preview git diffs and files using the diff4 CLI so users can securely review code changes and file content through diff4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djyde](https://clawhub.ai/user/djyde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to preview or share recent git diffs, staged changes, or selected UTF-8 text files through encrypted diff4 uploads. The skill returns the resulting URL and reminds users that recipients need the passphrase to decrypt the shared content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload git diffs or arbitrary UTF-8 text files to a configured diff4 server, which may expose sensitive or regulated content even though the payload is encrypted.

Mitigation: Require explicit user confirmation before every upload, verify the exact diff scope or file list, confirm the server URL, and avoid regulated content unless policy permits it.

Risk: Passphrases may be exposed if printed, passed visibly in shell arguments, or returned in agent-visible command output.

Mitigation: Avoid echoing or logging passphrases, do not pass them in visible command arguments, and share required decryption passphrases out of band.

## Reference(s):

- [diff4 default server](https://diff4.com)
- [ClawHub skill page](https://clawhub.ai/djyde/skills/diff4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and returned URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup guidance, upload commands, returned share URLs, and passphrase handling reminders.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

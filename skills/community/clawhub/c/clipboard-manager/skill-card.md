## Description:

Clipboard Manager stores clipboard history so users can search, pin, paste, and clear copied text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage local clipboard history, search previous copied text, pin frequently reused snippets, restore an item to the clipboard, or clear stored history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clipboard history can persist sensitive copied content, including passwords, API keys, private messages, financial details, or recovery codes, in plaintext.

Mitigation: Use only on a trusted single-user machine, clear history regularly, and prefer a hardened version with monitoring warnings, restrictive permissions or encryption, secret filtering, and expiration.

Risk: The skill monitors clipboard changes and stores copied text without clear access-control hardening.

Mitigation: Review the script before use and avoid running monitoring mode on shared, unmanaged, or high-sensitivity systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/clipboard-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update a local plaintext clipboard history file when its script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter, metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

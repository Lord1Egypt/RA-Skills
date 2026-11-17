## Description:

Create secure shareable self-destructing notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easyfloyd](https://clawhub.ai/user/easyfloyd)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to create encrypted, one-time-read notes from text supplied directly, through stdin, or from files and clipboard tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create notes containing highly sensitive secrets and send them to the configured FADNOTE_URL service.

Mitigation: Confirm the endpoint before use and require explicit confirmation before creating notes for credentials or other sensitive content.

Risk: Supplying secrets directly as command-line arguments can expose them through shell history or process listings.

Mitigation: Prefer piping content through stdin from a protected source instead of passing passwords, API keys, or private keys as arguments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/easyfloyd/skills/fadnote)
- [Project Homepage](https://github.com/easyFloyd/fadnote)
- [Live Service](https://fadnote.com)
- [Issue Tracker](https://github.com/easyFloyd/fadnote/issues)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Plain text URL or JSON with noteId, expiresIn, and decryptionUrl]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured FADNOTE_URL endpoint; input is limited to 1MB.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

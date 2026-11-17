## Description:

Manage Bring! shopping lists - view, add, remove items from shared grocery lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grewingm](https://clawhub.ai/user/grewingm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure access to Bring! and manage shared grocery lists by viewing, adding, and removing items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local CLI stores the Bring! password and session tokens in plaintext files.

Mitigation: Install only if comfortable with this storage model; prefer a version that prompts securely, uses an OS keychain or protected files, and provides clear secret removal.

Risk: The setup depends on an unpinned globally installed npm package.

Mitigation: Review the package before installation and prefer a pinned dependency with a lockfile for repeatable installs.

## Reference(s):

- [Bring API Reference](references/api.md)
- [bring-shopping NPM package source](https://github.com/foxriver76/node-bring-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Node.js CLI and Bring! account credentials to operate on shopping lists.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

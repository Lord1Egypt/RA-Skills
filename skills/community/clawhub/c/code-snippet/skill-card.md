## Description:

Code Snippet helps developers save, tag, search, list, retrieve, and optionally copy reusable code snippets from a local command-line store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain a personal library of reusable code snippets, including saving snippets with language and tag metadata, searching them, listing them, retrieving them, and copying snippet text when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snippet content is stored in plaintext at ~/.code_snippets.json.

Mitigation: Do not store secrets, credentials, or private keys as snippets; restrict the file to the local owner account.

Risk: The copy option writes snippet text to the system clipboard.

Mitigation: Use clipboard copying only for non-sensitive snippets and clear the clipboard after handling sensitive work.

Risk: Delete operations have no confirmation prompt or undo path.

Mitigation: Review snippet IDs before deletion and keep a backup of ~/.code_snippets.json when snippets are important.

## Reference(s):

- [ClawHub skill page: code-snippet](https://clawhub.ai/sxliuyu/skills/code-snippet)
- [ClawHub publisher profile: sxliuyu](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and code snippet text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write snippet records to ~/.code_snippets.json and optionally copy snippet text to the system clipboard.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

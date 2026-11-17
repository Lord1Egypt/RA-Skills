## Description:

Flatnotes 笔记服务 helps an agent create, search, retrieve, update, and delete Markdown notes in a configured Flatnotes instance, with support for full-text search and attachment-related API reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cal0rie](https://clawhub.ai/user/cal0rie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Markdown notes in a user-configured Flatnotes service, including saving generated reports, retrieving prior notes, and searching note content after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable Flatnotes credentials and note data, and the configured host is user supplied.

Mitigation: Install only when the Flatnotes host is trusted, use HTTPS, and prefer a revocable token or secret manager over storing a password in shell startup files.

Risk: Create, update, and delete operations can change or remove user notes.

Mitigation: Require explicit user confirmation before any operation that writes, updates, or deletes notes.

Risk: Passing passwords on the command line can expose secrets through shell history or process listings.

Mitigation: Avoid command-line passwords; use environment variables only when appropriate and prefer managed secrets.

## Reference(s):

- [Flatnotes API documentation](references/api_docs.md)
- [Skill homepage](https://cnb.cool/iceicc-ai-made/skills)
- [ClawHub skill page](https://clawhub.ai/cal0rie/skills/flatnotes-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-shaped API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include note titles, note content, search results, timestamps, and Flatnotes note URLs.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

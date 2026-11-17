## Description:

Community skill for parsing and executing local mailbox retrieval commands (`mail ...`) against a local backend with safe defaults, bounded output, and read-only constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmoraine](https://clawhub.ai/user/dmoraine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse `mail` requests, run allowed mailbox search and maintenance commands, and return concise email retrieval results with bounded output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates on Gmail mailbox data and can enable local indexing or embeddings of email content.

Mitigation: Use a read-only Gmail token, protect OAuth credentials, and review local storage and retention before use.

Risk: The release evidence flags an unpinned external install path.

Mitigation: Install from a pinned release or reviewed commit and avoid development extras for normal use.

Risk: `mail sync` performs mailbox maintenance work rather than a simple read-only search.

Mitigation: Run sync intentionally, understand that it updates the local index, and keep search limits bounded.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dmoraine/skills/clawinboxrag)
- [Commands](references/commands.md)
- [Setup](references/setup.md)
- [Security Guidance](references/security.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and recents output is bounded by configured limits; raw message bodies and secrets are not returned by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

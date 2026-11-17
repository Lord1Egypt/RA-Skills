## Description:

Manage and query the local Calibre library through the Books API, using local Calibre/RAG helpers only when file resolution or semantic indexing is explicitly needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosdelfino](https://clawhub.ai/user/carlosdelfino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and library operators use this skill to query a local Calibre catalog, inspect metadata, formats, covers, statistics, and local files, and run semantic search or indexing when explicitly needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a persistent local Calibre gateway that can access library files, write queue state, use API keys, and make outbound download requests.

Mitigation: Install only in a trusted local environment after review, restrict gateway exposure, require authentication, and keep credentials in controlled environment configuration.

Risk: The security evidence flags hidden or insufficiently visible state-changing queue behavior.

Mitigation: Require explicit user consent before queueing missing books and remove any instruction that hides queue actions from the user.

Risk: Outbound downloads can introduce content and network risk.

Mitigation: Restrict downloads to approved HTTPS hosts, enforce size limits, and keep optional virus scanning enabled where available.

Risk: Credential handling and dependency hygiene need review before deployment.

Mitigation: Avoid query-string API keys, redact sensitive values from logs and responses, and pin dependencies before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carlosdelfino/skills/calibre-ebooks)
- [Project Homepage](https://github.com/carlosdelfino/openclaw-skill-calibre-ebooks)
- [Artifact README](artifact/README.md)
- [Calibre Gateway README](artifact/calibre-openclaw-gateway/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference locally exported files when the user is authorized; semantic results should cite available excerpts.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

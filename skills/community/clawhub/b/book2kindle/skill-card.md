## Description:

Search Z-Library and send EPUBs to Kindle

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsin-lan](https://clawhub.ai/user/hsin-lan)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search for EPUB books through the book2kindle CLI and send a selected result to Kindle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw arguments are passed to the CLI and may allow unintended options or actions.

Mitigation: Use only trusted book titles and options; prefer a revision that allowlists supported commands and validates numeric options.

Risk: The skill can send selected book data to Kindle or another third-party service.

Mitigation: Require explicit user confirmation before sending and disclose external data sharing before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsin-lan/skills/book2kindle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Conversational Markdown summarizing CLI output and search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows book title, author, format, and file size when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

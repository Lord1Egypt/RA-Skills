## Description:

Helps agents publish Markdown documents and HTML pages to shareable byagent links and manage reader feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anup-a](https://clawhub.ai/user/anup-a)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to publish shareable documents or interactive pages, organize them into collections, and respond to reader comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages uploading finished work to an external service, potentially publicly without an explicit publication request.

Mitigation: Confirm the intended audience and visibility before publishing; use private access for internal material and do not upload secrets or personal data.

Risk: Guest publishing cannot keep internal material private.

Mitigation: Use an authenticated account with a restricted, revocable API key for private pages; do not publish sensitive work as a guest.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/anup-a/skills/byagent)
- [byagent homepage](https://byagent.dev)
- [byagent MCP integration](MCP.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown and HTML files, publishing commands, and shareable URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pages can be public or private; guest pages are temporary and public only.]

## Skill Version(s):

1.0.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

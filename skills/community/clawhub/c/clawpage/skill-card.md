## Description:

Share AI agent conversations as public web pages. Use when the user wants to share a conversation externally, export conversation history for documentation, or publish a chat session to a public URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imyelo](https://clawhub.ai/user/imyelo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use Clawpage to convert agent conversation sessions into reviewable, redacted clawpage YAML and publish them as public web pages when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation exports can expose sensitive internals such as reasoning, tool outputs, images, local paths, event metadata, credentials, private URLs, or personal contact details.

Mitigation: Use messages-only export by default unless process content is explicitly needed, redact sensitive values with [REDACTED], and inspect the full generated YAML before committing or publishing.

Risk: Public publishing can expose private or internal conversation content if a generated chat file is merged or deployed before review.

Mitigation: Keep exports on a dedicated branch, commit only the intended chat file, require explicit user confirmation before publishing, and use pull request review before merging.

Risk: Remote npm tooling invoked through npx can change behavior across versions.

Mitigation: Prefer pinned or local versions of the clawpage CLI tools when converting sessions for publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imyelo/skills/clawpage)
- [Clawpage project homepage](https://github.com/imyelo/clawpage)
- [Output Template](references/output-template.md)
- [Setup](references/setup.md)
- [OpenClaw Agent Profile](references/platforms/openclaw.md)
- [Unknown Platform Agent Profile](references/platforms/unknown.md)
- [Large File Handling](references/large-file.md)
- [Publish](references/publish.md)
- [Protect Sensitive Info](https://clawpage.yelo.ooo/chats/how-to-protect-sensitive-info/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML output and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces clawpage YAML files, redaction guidance, git branch and commit steps, and optional publishing instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

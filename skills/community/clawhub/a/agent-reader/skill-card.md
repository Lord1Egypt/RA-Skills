## Description:

Agent Reader helps AI agents convert Markdown and image inputs into styled HTML, PDF, DOCX, and slideshow outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebbfijsf](https://clawhub.ai/user/ebbfijsf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn raw Markdown reports, documents, and image collections into delivery-ready webpages, PDF or Word documents, and standalone slideshows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command uses an unpinned npm package, so the runtime code can change after review.

Mitigation: Pin the MCP command to the reviewed package version, such as agent-reader@1.3.7, or install from a controlled lockfile.

Risk: Converted documents and generated assets may be written to /tmp/agent-reader.

Mitigation: Avoid processing highly sensitive documents unless this output location and retention behavior are acceptable.

Risk: Generated HTML from untrusted Markdown or image inputs can carry content-rendering risk.

Mitigation: Review generated HTML before opening or sharing it, and run the skill with least privilege.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ebbfijsf/skills/agent-reader)
- [GitHub repository](https://github.com/ebbfijsf/agent-reader)
- [npm package](https://www.npmjs.com/package/agent-reader)
- [Glama listing](https://glama.ai/mcp/servers/ebbfijsf/agent-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [HTML, PDF, DOCX, standalone slideshow HTML, base64 file content, file paths, JSON status fields, and warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be written under /tmp/agent-reader or returned inline when requested.]

## Skill Version(s):

1.3.7 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

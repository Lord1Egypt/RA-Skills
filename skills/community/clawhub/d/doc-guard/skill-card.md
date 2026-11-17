## Description:

文档 is an agent skill for Markdown-oriented document processing, format conversion, content extraction, and collaboration workflows with claimed encrypted handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and automation users can use this skill to ask an agent to process Markdown, JSON, and text content, convert document formats, extract content, and coordinate document workflows. Sensitive or confidential documents should not be used unless the publisher supplies auditable encryption and access-control implementation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims encrypted document collaboration, but the security evidence says those security claims are unsupported by the artifact.

Mitigation: Do not rely on encryption, privacy, collaboration, or permission claims unless the publisher provides auditable implementation and key/access-control documentation.

Risk: The skill requests read, write, and command execution authority, which can affect local files and command behavior.

Mitigation: Use agent approval controls, restrict the skill to non-sensitive files, and require explicit approval before file writes or command execution.

Risk: Processing confidential documents could expose sensitive content if the claimed protections are not implemented.

Mitigation: Limit use to non-sensitive documents until the security model and data-handling behavior are independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown or JSON responses with optional file writes and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require API_KEY configuration and explicit authorization before file writes or command execution.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

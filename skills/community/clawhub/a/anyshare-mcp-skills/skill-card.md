## Description:

Guides an agent through AnyShare enterprise document search, upload and download, share-link parsing, and long-form writing workflows via the asmcp MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrrr](https://clawhub.ai/user/jerrrr)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and enterprise knowledge workers use this skill to work with AnyShare documents: finding files, confirming document identities, transferring files, parsing shared links, and generating long-form drafts from selected documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens may be exposed if pasted into chat or stored in plaintext local configuration.

Mitigation: Use only trusted AnyShare MCP endpoints, prefer local secure entry or a secret manager, restrict permissions on ~/.mcporter and mcporter.json, use narrowly scoped tokens where possible, and rotate any token previously pasted into a conversation.

Risk: The skill can access enterprise documents according to the user's AnyShare account and MCP server policy.

Mitigation: Deploy with trusted MCP servers and follow organizational authorization and data-classification rules before searching, downloading, uploading, sharing, or drafting from documents.

Risk: Incorrect document identifier or share-link handling can cause the agent to act on the wrong AnyShare file or folder.

Mitigation: Require explicit user confirmation before upload and download actions, display resolved paths when available, and preserve the documented distinction between full docid values and final-segment ids for writing workflows.

## Reference(s):

- [AnyShare](https://anyshare.aishu.cn)
- [AnyShare MCP troubleshooting](references/troubleshooting.md)
- [Security notes](SECURITY.md)
- [ClawHub skill page](https://clawhub.ai/jerrrr/skills/anyshare-mcp-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AnyShare document identifiers, share links, file paths, generated outlines, and generated draft text depending on the requested workflow.]

## Skill Version(s):

0.2.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

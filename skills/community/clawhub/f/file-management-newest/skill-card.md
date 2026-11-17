## Description:

File Management lets agents upload, list, download, share, delete, tag, and audit files stored in AgentPMT cloud storage through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to manage temporary and budget-scoped files in AgentPMT, including uploads, signed URLs, file downloads, metadata updates, sharing, access history, and expiration extension.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload files to AgentPMT cloud storage.

Mitigation: Use it only for files appropriate to store with AgentPMT, keep inputs minimal, and avoid placing secrets, wallet material, or payment headers in prompts or logs.

Risk: Delete and share actions can permanently remove files or create public access links.

Mitigation: Require explicit confirmation before delete or share actions, and use short share password expiration and use limits.

Risk: Related setup instructions and install commands can change after release.

Mitigation: Review before installing and prefer pinned or verified install commands for related setup skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/file-management-newest)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/file-management)
- [File Management Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [No-Account AgentAddress/x402 Setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, JSON]

**Output Format:** [Markdown instructions with JSON tool-call examples and remote tool JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote actions can return signed URLs, base64 file content for files up to 5MB, file metadata, share links, and access history; upload actions cover files up to 100MB.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

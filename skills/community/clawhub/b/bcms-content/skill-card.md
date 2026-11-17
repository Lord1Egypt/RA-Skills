## Description:

Run BCMS content operations from the command line; this thin CLI wraps the official @thebcms/client SDK for agents to create, update, delete, and list entries and upload media using a BCMS API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bcms](https://clawhub.ai/user/bcms)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to run deterministic BCMS entry and media operations from terminals, CI jobs, and agent workflows. It is suited for scripted content creation, updates, listing, deletion, and media uploads when a least-privilege BCMS API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can create, update, delete, and publish CMS content when used with a sufficiently privileged BCMS API key.

Mitigation: Use least-privilege API keys, separate keys by environment, and require human confirmation before production deletes or publishes.

Risk: BCMS API keys grant access to content operations and could expose or mutate CMS data if hard-coded, committed, or reused broadly.

Mitigation: Keep keys in environment variables or secret managers, rotate them regularly, and avoid committing key material to repositories.

Risk: Unpinned or remote package execution can introduce supply-chain and invocation risk.

Mitigation: Prefer the checked-in local CLI after reviewing dependencies and avoid unpinned npx execution in production workflows.

## Reference(s):

- [BCMS Agents Setup Guide](https://thebcms.com/agents)
- [BCMS Documentation](https://thebcms.com/docs)
- [BCMS MCP Guide](https://thebcms.com/docs/mcp)
- [Entries Reference](references/entries.md)
- [Media Reference](references/media.md)
- [Permissions Reference](references/permissions.md)
- [Properties Reference](references/properties.md)
- [MCP Reference](references/mcp.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples; CLI commands return status text and JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20 or newer, npm dependencies, and a BCMS_API_KEY with permissions for the target content or media operation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

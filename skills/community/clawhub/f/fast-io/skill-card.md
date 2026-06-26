## Description: <br>
Fast.io helps agents use shared workspaces to collaborate with agents and humans, manage files and shares, query documents with built-in AI, and coordinate workflow tasks through the Fast.io MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbalve](https://clawhub.ai/user/dbalve) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and teams use this skill to connect agents to Fast.io workspaces for file storage, branded sharing, workflow coordination, and document search. It is intended for agents that need authenticated access to Fast.io account, workspace, share, billing-adjacent, API-key, and raw API execution capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated control over Fast.io files, organizations, billing-adjacent actions, API keys, and raw API execution. <br>
Mitigation: Install only for agents that should manage Fast.io, and prefer scoped, expiring, read-only, or entity-limited credentials. <br>
Risk: Mutating or destructive operations can affect billing, ownership, API keys, account or organization closure, purge/delete behavior, and arbitrary authenticated execute calls. <br>
Mitigation: Require human confirmation before billing changes, ownership transfer, API key changes, account or organization closure, purge/delete operations, or any mutating execute call. <br>


## Reference(s): <br>
- [Fast.io homepage](https://fast.io) <br>
- [Fast.io REST API reference](https://api.fast.io/llms.txt) <br>
- [Platform guide](references/REFERENCE.md) <br>
- [ClawHub skill page](https://clawhub.ai/dbalve/fast-io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown, text] <br>
**Output Format:** [Markdown guidance with MCP tool calls, API examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and authenticated Fast.io credentials for most operations.] <br>

## Skill Version(s): <br>
1.233.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

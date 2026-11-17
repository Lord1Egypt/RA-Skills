## Description:

Operate the abracadabra local secrets vault through the abra CLI, abra serve, and abra MCP only when the user explicitly names abracadabra or abra, the abracadabra MCP is registered, or ABRA_KEY is already set for the project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[userdefault13](https://clawhub.ai/user/userdefault13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to access and manage secrets that a human has already scoped to the agent, including secret-name discovery, scoped secret loading, key management, health checks, local/LAN service use, sync, checkpoint, and consent-gated treasury payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched secrets may be written to disk through the documented private-file fallback, and server security evidence flags incomplete path-hardening for that path.

Mitigation: Prefer MCP or in-memory environment injection. Avoid the private-file fallback unless parent-directory symlink checks and cleanup are hardened and reviewed.

Risk: The skill can guide high-impact operations such as treasury payments, USB/LAN sync, restore, or license purchase flows.

Mitigation: Require explicit human confirmation before treasury payments, sync, restore, or license purchase actions.

Risk: Scoped vault API keys and secret payloads could be exposed if logged, pasted into chat, or passed through command-line arguments.

Mitigation: Keep API keys narrowly scoped and expiring, avoid printing secret values, and prefer flows that read credentials from environment variables or MCP approval rather than command arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/userdefault13/skills/abra)
- [Concierge Terminal](https://www.aarcadeghst.com/concierge/terminal)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Code]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to load allowlisted secret names into process environments or private files without exposing secret values in chat.]

## Skill Version(s):

1.0.9 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

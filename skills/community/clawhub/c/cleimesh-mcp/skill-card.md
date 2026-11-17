## Description:

Put the MCP tools an agent already uses behind CleiMesh, so each tool call runs under a signed, narrowable token and leaves a replayable receipt — a prompt injection cannot widen the grant, and you can prove afterwards what every tool did. Use when the user runs MCP servers in Claude Code, Cursor or another MCP client and wants to limit what a tool may touch, stop an injected tool call from reaching keys or the network, or produce an auditable, replayable record (audits, GDPR, LGPD). Also use after wrapping, when a CleiMesh-guarded MCP call is refused.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cleitonaugusto](https://clawhub.ai/user/cleitonaugusto)

### License/Terms of Use:

MIT OR Apache-2.0

## Use Case:

Developers who run MCP servers in Claude Code, Cursor, or another MCP client use this skill to prepare narrow CleiMesh token grants, register sandboxed or wrapped servers, and inspect or replay signed call receipts. It also explains that wrapped native servers retain their ordinary operating-system access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external executable and its security guarantees were not verified in this review.

Mitigation: Review and verify a specific installer release before running it, and pin the native server package version.

Risk: A wrapped native MCP server retains the ordinary operating-system access of its user.

Mitigation: Confirm the directories and network access being granted, and use process isolation when needed.

## Reference(s):

- [CleiMesh project](https://github.com/cleitonaugusto/cleimesh)
- [ClawHub release](https://clawhub.ai/cleitonaugusto/skills/cleimesh-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

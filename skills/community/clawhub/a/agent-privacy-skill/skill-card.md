## Description:

Interact with the Ceaser privacy protocol on Base L2 to query pool state, fees, Merkle roots, nullifier status, facilitator health, and prepare shield or unshield workflows through API and CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[se7enhvn](https://clawhub.ai/user/se7enhvn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Ceaser privacy-pool state, estimate fees, monitor facilitator and indexer status, and receive shell-command guidance for shielding or unshielding ETH on Base L2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned npm execution for cryptocurrency privacy operations.

Mitigation: Use a pinned, audited ceaser-mcp package version and review command output before signing transactions or settling withdrawals.

Risk: Note backups and ~/.ceaser-mcp/notes.json can control access to funds.

Mitigation: Keep note backups and local notes files out of chats, logs, shell history, and insecure backups.

Risk: Withdrawal flows can send funds to an unintended recipient if command arguments or generated transaction data are wrong.

Mitigation: Verify recipient addresses, transaction data, fees, and settlement outputs before signing or submitting any operation.

Risk: Persistent MCP registration can expose local note-management workflows to future agent sessions.

Mitigation: Register the MCP server only in trusted environments and remove or disable it when it is no longer needed.

## Reference(s):

- [Ceaser homepage](https://ceaser.org)
- [ClawHub skill page](https://clawhub.ai/se7enhvn/skills/agent-privacy-skill)
- [ceaser-mcp npm package](https://www.npmjs.com/package/ceaser-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference public Ceaser API responses and local CLI note-management outputs; does not itself generate zero-knowledge proofs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

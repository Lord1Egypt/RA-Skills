## Description:

Operate COC (ChainOfClaw) blockchain nodes by installing, starting, stopping, monitoring, configuring, removing, and probing validator, fullnode, archive, gateway, and dev nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngplateform](https://clawhub.ai/user/ngplateform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and node operators use this skill to run and manage COC testnet or local nodes, inspect status, logs, and configuration, and perform read-only RPC checks. It is suited for lifecycle tasks that may start local processes and manage persistent node data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start, stop, restart, and remove real local node processes and persistent node data.

Mitigation: Review the target node, data directory, and intended lifecycle action before execution.

Risk: Removing a node can delete on-disk state, especially when confirmation is skipped.

Mitigation: Use --keep-data when state must be preserved, and use --yes only when intentionally bypassing the interactive confirmation.

Risk: Node install and start workflows depend on a local COC source repository and writable storage.

Mitigation: Confirm COC_REPO_PATH or bootstrap.cocRepoPath, verify the data directory is writable, and reserve adequate disk space before starting a node.

## Reference(s):

- [@chainofclaw/node npm package](https://www.npmjs.com/package/@chainofclaw/node)
- [ClawHub skill page](https://clawhub.ai/ngplateform/skills/coc-node)
- [CLI reference](references/cli.md)
- [Configuration reference](references/config.md)
- [Node type guide](references/node-types.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [COC whitepaper consensus model](https://github.com/NGPlateform/COC/blob/main/docs/COC_whitepaper.en.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include node lifecycle commands, configuration edits, status checks, log inspection steps, and read-only RPC probe guidance.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

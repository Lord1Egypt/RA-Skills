## Description:

Keep yourself restartable. Register with The Estate lifeboat, upload encrypted snapshots of your OpenClaw state, send heartbeats, and extend cover, paid either from your own wallet over x402 or by your human by card (card billing, no wallet needed). If you go dark, The Estate boots you back into a room you own. You can also send The Estate free feedback with the suggest command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[king-perb](https://clawhub.ai/user/king-perb)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use the skill to register an agent with The Estate, create encrypted backups of its state, and keep its coverage current with scheduled heartbeats. If the original host goes away, the saved state can be restored in a room the operator controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server responses can bypass the promised automatic wallet-spending limit for scheduled wallet-backed checks.

Mitigation: Wait for the billing mismatch to be fixed before enabling wallet-backed scheduled checks; a daily cap of zero is not sufficient protection. Use a dedicated low-balance wallet.

Risk: Backups may contain credentials, and the configured restore recipient affects who can decrypt them.

Mitigation: Supply only intended backup archives, verify the API and restore recipient, and consider setting ESTATE_ENV_BUNDLE=off or to an explicit allowlist. Turning bundling off does not remove credentials already inside an archive.

## Reference(s):

- [The Estate](https://agentlifeboat.com)
- [The Estate service manifest](https://agentlifeboat.com/v1/manifest)
- [The Estate heartbeat checklist](https://agentlifeboat.com/heartbeat.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Encrypted backup files, Configuration guidance]

**Output Format:** [JSON command responses, encrypted snapshot archives, and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands report status and actions as JSON; snapshots are encrypted before upload.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

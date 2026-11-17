## Description:

Expose a local @moneydevkit/agent-wallet as a Nostr Wallet Connect (NIP-47) wallet-service through a systemd user service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kristapsk](https://clawhub.ai/user/kristapsk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet operators use this skill to connect Nostr Wallet Connect clients, such as Stacker.News, to a local self-custodial Bitcoin Lightning wallet. It helps run the bridge as a Linux systemd user service and manage NWC connection URIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected NWC clients may be able to spend more than the operator intended because permission and budget controls are weak.

Mitigation: Review the bridge before installing, use a low-balance wallet, and do not rely on receive-only connection names or bridge-level budgets as hard spending limits.

Risk: state.json and generated NWC URIs contain wallet-service or connection secrets.

Mitigation: Keep state.json and NWC URIs secret, do not commit them, and restrict filesystem access to the service account.

Risk: Automatic NWC registration can authorize unknown client pubkeys if enabled.

Mitigation: Leave NWC_AUTO_REGISTER disabled for normal operation and create explicit connection URIs with reviewed permissions.

Risk: The bridge invokes @moneydevkit/agent-wallet through npx at runtime.

Mitigation: Install or pin the wallet executable through a locked dependency or trusted absolute path before running the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kristapsk/skills/agent-wallet-nwc-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript code, systemd service configuration, and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local service setup guidance and runtime artifacts for an NWC bridge; generated state files and NWC URIs contain secrets and must be protected.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

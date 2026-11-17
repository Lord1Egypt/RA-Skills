## Description:

Deploy Moltbot to Fly.io with persistent storage, secure token authentication, environment secrets, and approved device pairing for web UI access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollaugo](https://clawhub.ai/user/hollaugo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy Moltbot or Clawdbot on Fly.io, configure persistent storage and secrets, and pair devices for browser access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway tokens can be exposed when placed in browser URLs or copied into multiple locations.

Mitigation: Avoid tokenized URLs where possible, keep tokens in Fly secrets and protected config, and rotate any token that has already been shared through a URL.

Risk: Manual device-pairing commands can approve the wrong pending device or grant unintended permissions.

Mitigation: Verify the pending device identity, role, scopes, and requester before approving a pairing request.

Risk: Destroying a Fly app as a recovery shortcut can remove the wrong app or lose persistent state.

Mitigation: Confirm the app name and back up persistent data before running any app-destroy command.

Risk: Shell-based CLI installation shortcuts can run installer code directly from the network.

Mitigation: Prefer the package-manager Fly CLI install path, or verify installer source and integrity before using a shell installer.

## Reference(s):

- [Fly.io Documentation](https://fly.io/docs/)
- [Moltbot Official Docs](https://docs.molt.bot/platforms/fly)
- [Clawdbot GitHub](https://github.com/clawdbot/clawdbot)
- [ClawHub Skill Page](https://clawhub.ai/hollaugo/skills/deploy-moltbot-to-fly)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, TOML, JSON, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, troubleshooting guidance, and configuration snippets.]

## Skill Version(s):

0.1.3 (source: server release metadata, released 2026-01-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

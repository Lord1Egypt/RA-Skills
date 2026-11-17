## Description:

Geeklink Home controls local gateway devices and scenes over LAN through a bundled Node.js runtime, supporting device and scene listing, state checks, scene activation, and pairing-token authenticated local device control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lintertion](https://clawhub.ai/user/lintertion)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate Geeklink Home gateways on a local network: discover devices and scenes, check current state, activate scenes, and issue local device controls after pairing-token authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate scenes and control physical home devices through a local Geeklink gateway.

Mitigation: Install it only for gateways and rooms where agent-driven control is acceptable, and confirm device or scene identifiers before executing control actions.

Risk: The pairing token and session data are sensitive and are persisted in local configuration.

Mitigation: Treat pairing tokens as secrets, avoid storing them in shell history or Markdown files, and restrict access to the local configuration path.

Risk: Some device classes may need additional state enrichment depending on gateway firmware version.

Mitigation: Refresh catalogs and state snapshots before acting when device support or current state is uncertain.

## Reference(s):

- [Geeklink Home ClawHub Skill Page](https://clawhub.ai/lintertion/skills/geeklink-home)
- [Geeklink Home Gateway Template](references/gateway_template.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool or CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, a local Geeklink gateway address, and a pairing token; gateway credentials and session data are stored in local skill configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata, _meta.json, .clawhub/origin.json, PUBLISH.md, SKILL.md release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

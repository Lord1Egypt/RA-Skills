## Description:

Installs ControlClaw for OpenClaw or connects an agent to an existing firewall, routing its traffic through configurable access rules and approval controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madawaldos](https://clawhub.ai/user/madawaldos)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use the skill to install a local ControlClaw firewall, connect an agent to an existing firewall, or set up a private firewall for several agents. It guides users through setup choices, pairing, firewall modes, and panel configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags repeated unpinned npm commands that may fetch and run changing code, including during privileged setup or pairing; no malicious intent is established.

Mitigation: Review the package identity and version before running npm commands, require explicit user approval for privileged setup, and keep pairing codes out of command arguments.

Risk: The scan is partial because two local references could not be resolved, so the evidence is incomplete.

Mitigation: Resolve the missing references and repeat the scan before relying on its security review.

## Reference(s):

- [ControlClaw project homepage](https://github.com/madarco/controlclaw)
- [ControlClaw standalone documentation](https://github.com/madarco/controlclaw/tree/main/docs/standalone)
- [ControlClaw firewall ClawHub release](https://clawhub.ai/madawaldos/skills/controlclaw-firewall)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup guidance and commands vary by requested firewall configuration and available system capabilities.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

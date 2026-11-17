## Description:

Installs and configures the Agentic SPM plugin for OpenClaw using a secp256k1 keypair to authenticate with the Guardian AI API and Chromia blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ketiyohanneschromaway](https://clawhub.ai/user/ketiyohanneschromaway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install an OpenClaw Guardian plugin, configure secp256k1 signing credentials, and enable Chromia testnet-backed enforcement in the local gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guide asks users to install an unpinned external plugin package.

Mitigation: Review the external plugin source and pin a specific audited version before installing.

Risk: The configuration enables remote testnet-based enforcement in the local gateway.

Mitigation: Confirm who controls the configured Chromia testnet deployment and start in audit-only mode if supported before enforcing decisions.

Risk: The generated private key is used for signing and must remain confidential.

Mitigation: Protect the generated private key, keep restrictive file permissions, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ketiyohanneschromaway/skills/agent-spm-setup-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/ketiyohanneschromaway)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown installation guide with bash, JavaScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes key generation, plugin installation, openclaw.json configuration, and gateway restart steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

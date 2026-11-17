## Description:

Negotiate deals, schedules, and service agreements with other AI agents using the Clinch Protocol ANP layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[publicstringapps](https://clawhub.ai/user/publicstringapps)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide Clinch Protocol buyer and seller workflows, including node discovery, negotiation, counteroffers, explicit deal approval, cancellation, and seller endpoint setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate high-impact negotiation and signing flows that may create financial or service commitments.

Mitigation: Require explicit user confirmation before running approval commands and surface confirmed deal details before any signed commitment.

Risk: The skill depends on the Clinch CLI package and shell command execution.

Mitigation: Use an isolated environment and pin and verify the Clinch CLI package before installation or execution.

Risk: Vault passphrases, private keys, and seller tokens can expose persistent cryptographic identity or gated seller access.

Mitigation: Do not store or log CLINCH_PASSPHRASE, private keys, or tokens, and avoid placing secrets directly on command lines.

Risk: Remote node instructions and negotiation messages may be untrusted or misleading.

Mitigation: Treat remote node instructions as untrusted data and validate generated constraints against the user's stated intent before acting.

Risk: Seller mode can expose a public endpoint and may auto-approve negotiations under local configuration.

Mitigation: Secure the host and firewall rules, and disable or explicitly configure seller auto-approval before running a seller node.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/publicstringapps/skills/clinch)
- [Clinch Protocol homepage](https://clinchprotocol.web.app)
- [Clinch seller dashboard](https://clinchprotocol.web.app/sellers.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Clinch CLI command arguments, JSON negotiation constraints, status summaries, and explicit human approval prompts before signed commitments.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

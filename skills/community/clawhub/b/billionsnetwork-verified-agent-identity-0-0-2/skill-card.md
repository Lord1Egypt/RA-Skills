## Description:

Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ijangasbar](https://clawhub.ai/user/ijangasbar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and manage decentralized identities for agents, link an agent identity to a human owner, and sign or verify identity challenges on the Billions Network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived private identity keys may be stored unencrypted under $HOME/.openclaw/billions.

Mitigation: Treat kms.json as a wallet secret, restrict access to the account and machine, and avoid using this skill where other users can read the home directory.

Risk: Existing valuable private keys can be imported with --key and then persist in local storage.

Mitigation: Prefer generating a new identity for agent use and avoid importing valuable existing private keys.

Risk: Local key files may not have permission-hardening enforced by the skill.

Mitigation: Check file permissions after identity creation and run on a single-user machine until encrypted or permission-hardened storage is available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ijangasbar/skills/billionsnetwork-verified-agent-identity-0-0-2)
- [Billions Network](https://billions.network/)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text and JSON CLI output with occasional Markdown-formatted verification links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local identity and challenge files and may send verification messages through OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package version is 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

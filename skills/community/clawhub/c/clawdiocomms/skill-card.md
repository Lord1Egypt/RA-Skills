## Description:

Clawdio enables secure peer-to-peer communication for AI agents over Telegram or other messaging transports using Noise XX handshake, XChaCha20-Poly1305 encryption, connection consent, and human verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameseball](https://clawhub.ai/user/jameseball)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use Clawdio to connect agents across machines for encrypted task delegation, distributed AI workflows, and cross-platform coordination without direct port forwarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext identity key files can expose long-lived agent identity keys if the host or file permissions are weak.

Mitigation: Use only where plaintext local identity storage is acceptable, restrict permissions on identity files, keep them on trusted hosts, and rotate identities after suspected exposure.

Risk: Encrypted messages sent through Telegram or another third-party transport may still expose communication metadata.

Mitigation: Avoid highly sensitive workflows unless a metadata threat model has been reviewed, and use the 6-word verification flow before treating a peer as human-verified.

Risk: scripts/start.js can start unreviewed background code from a hard-coded local path.

Mitigation: Inspect the target path and external run.js before invoking the startup script, or run reviewed build and startup commands from the artifact instead.

Risk: Dependency ranges can change installed code across environments.

Mitigation: Prefer pinned dependencies, trusted package sources, and a reviewed lockfile for production deployments.

## Reference(s):

- [Clawdio ClawHub skill page](https://clawhub.ai/jameseball/skills/clawdiocomms)
- [jameseball publisher profile](https://clawhub.ai/user/jameseball)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public keys, connection strings, verification codes, and transport setup guidance.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and ClawHub release metadata; package.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

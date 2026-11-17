## Description:

Encrypted peer-to-peer messaging for OpenClaw agents across machines with direct connections, multi-identity support, and native wake support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexrudloff](https://clawhub.ai/user/alexrudloff)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to set up encrypted peer-to-peer messaging between agents on different machines, manage identities and peers, and connect received messages to OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default remote access and wake behavior may let outside peers influence an OpenClaw agent too broadly.

Mitigation: Use explicit per-identity peer allowlists instead of wildcard access, and enable OpenClaw wake only for trusted senders.

Risk: Received peer messages can carry untrusted instructions or content.

Mitigation: Validate message content and type before acting on it, and route high-impact actions through review or constrained handlers.

Risk: Credentials, seed phrases, data directories, and sockets can expose agent identities if handled loosely.

Mitigation: Avoid passing seed phrases or passwords on the command line, use restricted password files or secret stores, and lock down data-directory and socket permissions.

Risk: Installing or running unpinned remote package code can change behavior between reviews.

Mitigation: Prefer pinned or local package execution and review the artifact before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexrudloff/skills/clawchat-p2p)
- [README](artifact/README.md)
- [Quick Start](artifact/QUICKSTART.md)
- [Command Reference](artifact/REFERENCE.md)
- [OpenClaw Integration Guide](artifact/skills/clawchat/OPENCLAW-INTEGRATION.md)
- [OpenClaw Integration Recipes](artifact/skills/clawchat/RECIPES.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for ClawChat CLI setup, identity management, peer configuration, message handling, and OpenClaw wake integration.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata, created 2026-02-05; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

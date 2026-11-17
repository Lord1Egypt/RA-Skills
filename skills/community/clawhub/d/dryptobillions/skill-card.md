## Description:

Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adhamelswesy](https://clawhub.ai/user/adhamelswesy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to create and manage Billions Network decentralized identities for agents, link an agent DID to a human owner, sign identity challenges, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and stores long-lived private keys for agent identities under $HOME/.openclaw/billions.

Mitigation: Use a disposable or low-value identity, restrict filesystem access to the key directory, and review key-storage handling before using it for important identity workflows.

Risk: The skill can send signed identity material through OpenClaw messages and relies on remote services and npm dependencies.

Mitigation: Review the destination, use a reviewed and pinned release, and install only when the listed services and dependencies are acceptable for the intended identity workflow.

## Reference(s):

- [Billions Network](https://billions.network/)
- [DryptoBillions on ClawHub](https://clawhub.ai/adhamelswesy/skills/dryptobillions)
- [adhamelswesy ClawHub Profile](https://clawhub.ai/user/adhamelswesy)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text and JSON responses with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local identity files under $HOME/.openclaw/billions and may send signed identity material through OpenClaw messages.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

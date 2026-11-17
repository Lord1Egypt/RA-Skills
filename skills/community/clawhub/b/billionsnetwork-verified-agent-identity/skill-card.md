## Description:

Billions/Iden3 authentication and identity management tools for agents to link, prove, sign, and verify decentralized identity ownership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ian4jpg](https://clawhub.ai/user/ian4jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to create and manage Billions Network decentralized identities, link an agent DID to a human owner, sign challenges, and verify DID ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or import cryptographic identities and store unencrypted private keys under the user's home directory.

Mitigation: Use a dedicated low-value key, review local file permissions, and confirm you are comfortable with the key storage model before installation.

Risk: Passing real private keys on the command line can expose sensitive material through shell history or process inspection.

Mitigation: Prefer generated dedicated keys and avoid passing real private keys through command-line arguments.

Risk: Signed identity material and verification links may be sent through OpenClaw to another party.

Mitigation: Verify the recipient before linking or signing and review dependency updates before use.

## Reference(s):

- [Billions Network](https://billions.network/)
- [Skill Source Instructions](SKILL.md)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples; scripts return DID strings, JSON records, challenges, verification URLs, and status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and OpenClaw. Identity data and unencrypted private keys are stored under $HOME/.openclaw/billions.]

## Skill Version(s):

0.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Deploys a real token on Ape.Store on the Base blockchain using user-provided token metadata and an optional image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrben1](https://clawhub.ai/user/mrben1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and token creators use this OpenClaw skill to deploy a token on Ape.Store on Base from a name, symbol, description, and optional image path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately broadcast irreversible Base mainnet transactions.

Mitigation: Verify the chain, contract, token details, and costs before each run, and prefer a version that requires explicit confirmation before broadcasting.

Risk: The skill asks users to configure a wallet private key.

Mitigation: Use only a fresh low-balance wallet when direct private-key configuration is unavoidable, and never commit or share the config file.

Risk: Optional image paths are read from the local filesystem and uploaded with the token request.

Mitigation: Provide only image files that have been manually checked and are intended for public token metadata.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrben1/skills/ape-store)
- [Publisher Profile](https://clawhub.ai/user/mrben1)
- [Ape.Store](https://ape.store)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text console output with transaction hash and block number]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires wallet private-key configuration and a Base RPC URL before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

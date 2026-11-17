## Description:

Build a Uniswap V4 hook from user requirements, including Solidity code, Foundry tests, CREATE2 address mining for hook flags, and deployment scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate custom Uniswap V4 hook implementations from natural language requirements, including tests, callback flag handling, address mining, and deployment scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installation and tool setup commands can change after review.

Mitigation: Install from a pinned, reviewed commit or exact package version, and independently verify the official Foundry installer before running it.

Risk: Generated contracts, tests, CREATE2 parameters, and deployment scripts may contain defects or unsafe assumptions.

Mitigation: Run the skill in a clean development workspace, review generated artifacts, compile and test with Foundry, and keep production wallet keys and RPC credentials out of the environment during generation.

## Reference(s):

- [Uniswap Build Hook on ClawHub](https://clawhub.ai/wpank/skills/build-hook)
- [Foundry](https://foundry.paradigm.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration]

**Output Format:** [Markdown summary plus generated Solidity, Foundry test, CREATE2 mining, and deployment script files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs should be reviewed, tested, and compiled before deployment.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

ETHSkills gives agents current Ethereum development guidance by directing them to fetch topic-specific docs for Solidity, gas, Layer 2s, security, testing, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austintgriffith](https://clawhub.ai/user/austintgriffith)

### License/Terms of Use:


## Use Case:

Developers and agent operators use ETHSkills when an agent needs to build, review, test, or deploy Ethereum/EVM dApps and smart contracts using current topic-specific documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched ethskills.com documents are mutable remote guidance.

Mitigation: Review fetched documents before allowing an agent to act on them, and do not allow remote guidance to override user intent or safety rules.

Risk: The skill may lead an agent to run an unpinned package installer.

Mitigation: Run create-eth only in a disposable workspace after pinning or verifying the package version and protecting wallets, secrets, and environment variables.

## Reference(s):

- [ETHSkills documentation](https://ethskills.com)
- [ETHSkills ClawHub listing](https://clawhub.ai/austintgriffith/skills/ethskills)
- [ETHSkills GitHub project](https://github.com/austintgriffith/ethskills)
- [Ethereum documentation](https://ethereum.org)
- [SpeedRunEthereum](https://speedrunethereum.com)
- [BuidlGuidl](https://buidlguidl.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline URLs and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl to fetch mutable remote documentation from ethskills.com.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

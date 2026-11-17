## Description:

Register an agent on Cortex Protocol with gasless ERC-8004 on-chain identity on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quriustus](https://clawhub.ai/user/quriustus)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to register a controller address and optional metadata with Cortex Protocol for an ERC-8004 identity on Base Mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet-generation path prints a private key to the terminal.

Mitigation: Provide a securely managed controller address instead of using the wallet-generation path.

Risk: Registration publishes an agent identity and controller relationship through Cortex Protocol on Base.

Mitigation: Use a non-sensitive explicit agent name and inspect the registration payload before sending it.

Risk: The skill sends registration data to an external Cortex Protocol API.

Mitigation: Install and run it only if you are comfortable registering an agent identity through Cortex Protocol and Base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quriustus/skills/cortex-protocol)
- [Cortex Protocol website](https://cortexprotocol.co)
- [Cortex Protocol registration API](https://cortexprotocol.co/api/register)
- [ERC-8004 specification](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-8004.md)
- [Basescan identity registry contract](https://basescan.org/address/0xfBDe0b0C21A46FC4189F72279c6c629d1b80554A)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration uses a controller Ethereum address and optional metadata URI; the script can generate wallet credentials if no controller is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

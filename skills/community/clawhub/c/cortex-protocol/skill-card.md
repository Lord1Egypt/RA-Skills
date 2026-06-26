## Description: <br>
Register an agent on Cortex Protocol with a gasless ERC-8004 identity on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quriustus](https://clawhub.ai/user/quriustus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to register a public on-chain agent identity, optionally using an existing controller address and storing the returned token and transaction details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default wallet-generation path can print a private key in the terminal. <br>
Mitigation: Use a trusted wallet to create or manage the controller address and pass only the public address to the script; avoid shared terminals, CI, recorded sessions, and agent logs when private keys may be displayed. <br>
Risk: Agent names, controller addresses, tokens, and transactions become persistent public on-chain records. <br>
Mitigation: Use a pseudonymous agent name instead of the hostname default and review the registration details before submitting them. <br>


## Reference(s): <br>
- [Cortex Protocol website](https://cortexprotocol.co) <br>
- [Cortex Protocol on ClawHub](https://clawhub.ai/quriustus/cortex-protocol) <br>
- [ERC-8004 Trustless Agents](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-8004.md) <br>
- [BaseScan identity registry contract](https://basescan.org/address/0xfBDe0b0C21A46FC4189F72279c6c629d1b80554A) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public registration details such as controller address, token ID, and transaction hash.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

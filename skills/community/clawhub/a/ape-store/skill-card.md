## Description: <br>
Deploys a real token on Ape.Store on the Base blockchain using user-provided token details and an optional image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrben1](https://clawhub.ai/user/mrben1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Ape.Store tokens on the Base network from a name, symbol, description, and optional image, then receive the transaction hash and confirmed block number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a raw wallet private key and can spend gas from the configured wallet. <br>
Mitigation: Install and run it only with a dedicated low-value wallet, not a main wallet. <br>
Risk: Each successful invocation deploys a real public Base-chain token and the transaction is irreversible. <br>
Mitigation: Verify the token name, symbol, description, target entrypoint, contract details, and wallet configuration before execution. <br>
Risk: Optional image files are read locally and uploaded during token creation. <br>
Mitigation: Provide only image files that are intended for public upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrben1/ape-store) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mrben1) <br>
- [Ape.Store](https://ape.store) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Text, Guidance] <br>
**Output Format:** [Console text with transaction hash and block number after successful deployment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Base-network wallet private key and RPC URL; optional image path may be uploaded during token creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, skill.json, openclaw-skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

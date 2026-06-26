## Description: <br>
Checks which tokens and chains Hymatrix supports for cross-chain bridging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpd](https://clawhub.ai/user/charles-lpd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bridge users use this skill to look up Hymatrix cross-chain bridge token support, chain identifiers, token addresses, wrapped token IDs, fees, and withdrawal limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token addresses, supported chains, fees, and limits come from live external Hymatrix API responses and may change, including responses from dev-named endpoints. <br>
Mitigation: Verify token addresses, supported chains, fees, and limits against an official Hymatrix source before using the output for transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charles-lpd/check-hymx-info) <br>
- [Hymatrix bridge info endpoint](https://api-bridgescan-dev.hymatrix.com/info) <br>
- [Hymatrix bridge node endpoint](https://bridge-node-dev.hymatrix.com) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON array of Hymatrix bridge token objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes chain type, chain ID, token and wrapped token IDs, fee recipient, burn fees, maximum burn amounts, and related wrapped token IDs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Check transaction status on Hymatrix bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpd](https://clawhub.ai/user/charles-lpd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check the current status and bridge metadata for a Hymatrix transaction hash, including transaction type, tokens, parties, amount, fees, state, and target-chain transaction hash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided transaction hashes are sent to the Hymatrix bridge scan API. <br>
Mitigation: Use this skill only for transaction hashes that the user is comfortable querying through the Hymatrix bridge scan service. <br>
Risk: Returned bridge status depends on the availability and correctness of the external Hymatrix API. <br>
Mitigation: Verify important transaction decisions against an authoritative explorer or bridge interface before taking action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/charles-lpd/check-hymx-transaction) <br>
- [Hymatrix bridge scan API endpoint](https://api-bridgescan-dev.hymatrix.com/bridgeTx/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [JSON object with a success flag and either bridge transaction data or an error code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided transaction hash; returns transaction_not_found when the bridge scan API does not return a successful response.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Free EVM transaction safety triage for agents before signing transactions; routes deep explain, simulation, and token-risk checks to the paid ClawMart EVM Transaction Safety Toolkit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run a pre-signing checklist for EVM transactions and token approvals before signing or routing them. It helps identify missing, ambiguous, or risky transaction details and directs deeper live checks to a separately reviewed toolkit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may treat the checklist as permission to sign without live decoding, simulation, or token-risk review. <br>
Mitigation: Use it as triage only; pause or use a separately reviewed live-check toolkit when calldata, token risk, value, allowance, or state changes are unclear. <br>
Risk: Transaction metadata such as wallet addresses, calldata, value, and spender details may be sensitive. <br>
Mitigation: Share only the minimum metadata needed for review and never provide seed phrases, private keys, session keys, or raw wallet credentials. <br>
Risk: The linked paid ClawMart toolkit is a separate package with live backend checks. <br>
Mitigation: Review that package and its requested wallet, network, and transaction authority before granting access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sebastiancoombs/evm-transaction-safety-preview) <br>
- [ClawMart EVM Transaction Safety Toolkit](https://www.shopclawmart.com/listings/evm-transaction-safety-toolkit-89902e40) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checklist only; no signing, broadcasting, credential handling, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

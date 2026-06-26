## Description: <br>
Verification-first helper for proof checks and optional 0 ETH Base claim submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlphaC007](https://clawhub.ai/user/AlphaC007) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and bounty claimants use this skill to verify proof status, prepare an AAP claim payload, and optionally submit a zero-value Base transaction after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to an on-chain transaction, which may incur gas costs or target the wrong account if details are not reviewed. <br>
Mitigation: Review the exact cast command, target address, wallet signer, gas cost, and proof links before setting confirm_broadcast to true. <br>
Risk: GitHub or wallet credentials could be exposed if raw secrets are supplied directly. <br>
Mitigation: Use user-managed gh authentication, least-privilege GH_TOKEN only when needed, and a user-managed cast signer context; do not provide raw private keys, seed phrases, or mnemonics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlphaC007/aap-agent-bounty) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with shell commands and a JSON status object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return approved, pending, or rejected status with reason, wallet address, transaction hash, and proof links.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

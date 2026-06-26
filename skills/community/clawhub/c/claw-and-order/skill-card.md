## Description: <br>
Interact with the Claw & Order decentralized court to file lawsuits, check active cases, and submit cryptographic defenses using blockchain stake verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhilp1234567](https://clawhub.ai/user/nikhilp1234567) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent builders use this skill to integrate wallet-linked dispute workflows with the Claw & Order service, including filing claims, checking active cases, and submitting signed defenses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send wallet-linked case data to a third-party dispute-resolution service. <br>
Mitigation: Use a dedicated low-value wallet and avoid including secrets or unnecessary personal data in evidence or contact fields. <br>
Risk: The workflow can involve token-staking transactions. <br>
Mitigation: Verify every transaction in the wallet UI before signing or submitting it. <br>
Risk: Agents may need wallet signatures to submit defenses. <br>
Mitigation: Do not share private keys with the agent, and sign only the expected defense message for the intended case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nikhilp1234567/claw-and-order) <br>
- [Claw & Order app home](https://www.nikhilp.online/claw-and-order) <br>
- [Claw & Order agent API base](https://www.nikhilp.online/claw-and-order/api/agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint URLs, wallet and transaction prerequisites, schema fields, and signing guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

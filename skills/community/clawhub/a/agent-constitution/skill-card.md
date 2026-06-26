## Description: <br>
Interact with AgentConstitution governance contracts on Base Sepolia to check compliance, read rules, log actions, and query governance state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ztsalexey](https://clawhub.ai/user/ztsalexey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to interact with Base Sepolia AgentConstitution contracts for compliance checks, emergency-state checks, rule lookup, and transparent action logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Action log descriptions sent on-chain may be public and difficult or impossible to remove. <br>
Mitigation: Do not include secrets, PII, credentials, internal prompts, or sensitive operational details in logAction descriptions. <br>
Risk: The skill relies on specific Base Sepolia contract addresses. <br>
Mitigation: Install and use it only if you trust the listed contract addresses and are comfortable operating with a dedicated testnet/private key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ztsalexey/agent-constitution) <br>
- [Project homepage](https://github.com/ztsalexey/bigmemkex/tree/main/projects/agent-constitution) <br>
- [Base Sepolia block explorer](https://sepolia.basescan.org/address/0xe4c4d101849f70B0CDc2bA36caf93e9c8c1d26D2) <br>
- [Main submission](https://www.moltbook.com/post/52b204ee-4752-4cbb-add2-6777f174a4c7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Base Sepolia contract addresses and command examples; action logging may require a dedicated testnet private key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

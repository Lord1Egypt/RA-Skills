## Description: <br>
Enable quantum-resistant encryption and secret management for blockchain applications with the CIFER SDK, including ML-KEM-768 encryption, wallet integration, multi-chain discovery, file encryption jobs, and transaction intents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohsinriaz17](https://clawhub.ai/user/mohsinriaz17) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to integrate CIFER SDK encryption workflows into blockchain applications, including payload encryption, file encryption jobs, key authorization, on-chain commitments, and wallet-controlled transaction intents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents blockchain wallet signatures and transaction intents that could authorize real on-chain actions. <br>
Mitigation: Review every signature and transaction intent before execution, and start with least-privileged or test wallets. <br>
Risk: Server-side examples rely on a PRIVATE_KEY environment variable. <br>
Mitigation: Store private keys in a secrets manager or equivalent protected secret store, and avoid exposing them in logs, prompts, or source control. <br>
Risk: File encryption and decryption workflows send data to the Blackbox service. <br>
Mitigation: Confirm the service's data-handling and retention policies before sending regulated or highly sensitive files. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/mohsinriaz17/cifer-sdk) <br>
- [CIFER SDK npm package](https://www.npmjs.com/package/cifer-sdk) <br>
- [CIFER SDK GitHub repository](https://github.com/cifer-security/cifer-sdk) <br>
- [Blackbox API endpoint](https://blackbox.cifer.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with TypeScript examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes SDK installation commands, wallet integration examples, encryption and decryption flows, transaction intent guidance, and file job workflows.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

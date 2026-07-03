## Description: <br>
Encrytion Decryption Toolkit helps agents call AgentPMT-hosted cryptographic tools to generate random values, compute hashes and HMACs, create signatures, and perform AES-256-GCM encryption or decryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs remote cryptographic utility calls for token generation, checksums, HMAC validation, signatures, or AES-256-GCM encryption and decryption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote cryptographic operations may send raw keys, secrets, private keys, plaintext, or decrypted data to AgentPMT. <br>
Mitigation: Use the skill only when AgentPMT is trusted for the exact material involved, and avoid production secrets or regulated data without explicit approval and a retention/logging policy. <br>
Risk: AES-256-GCM encryption depends on correct key size and unique IV use. <br>
Mitigation: Provide 32-byte keys, use 12-byte IVs, and never reuse the same IV with the same key. <br>
Risk: Remote schema or examples may drift from the generated artifact. <br>
Mitigation: Fetch live schema or instructions before production integrations when parameters, enum values, outputs, or examples are unclear. <br>


## Reference(s): <br>
- [Generated action schema](artifact/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/encrytion-decryption-toolkit) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/encrytion-decryption-toolkit) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers six remote actions: generate, hash, hmac, sign, encrypt, and decrypt.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

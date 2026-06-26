## Description: <br>
Store and fetch credentials securely at runtime via AgentLair Vault REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hawkaa](https://clawhub.ai/user/hawkaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to store, fetch, rotate, list, and revoke credentials through AgentLair Vault instead of keeping third-party API keys in local agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to handle secrets through AgentLair Vault, so users must trust AgentLair with the credentials they store unless they use client-side encryption. <br>
Mitigation: Install only after accepting that trust relationship, and use the documented client-side encryption option when zero-knowledge handling is required. <br>
Risk: AGENTLAIR_API_KEY grants access to vault operations and is highly sensitive. <br>
Mitigation: Keep AGENTLAIR_API_KEY out of committed files and long-lived shared environments, and protect it with the same care as other production credentials. <br>
Risk: Metadata can accidentally disclose sensitive context even when it is not the secret value. <br>
Mitigation: Store only labels, service names, and non-secret operational hints in metadata. <br>
Risk: Rotate and delete operations can change or remove credentials that agents depend on. <br>
Mitigation: Require explicit user confirmation before rotating or deleting credentials, and use version history for rollback where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hawkaa/agentlair-vault) <br>
- [AgentLair homepage](https://agentlair.dev) <br>
- [AgentLair security documentation](https://agentlair.dev/security) <br>
- [AgentLair trust model blog](https://agentlair.dev/blog) <br>
- [agentlair-vault-crypto source](https://github.com/piiiico/agentlair-vault-crypto) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for using AgentLair Vault REST endpoints with AGENTLAIR_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

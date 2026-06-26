## Description: <br>
Provides domain-anchored cryptographic identity verification for AI agents using ES256 JWTs, TOFU key pinning, revocation, and delegation chain checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaschadub](https://clawhub.ai/user/jaschadub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement and verify cryptographic identity for AI agents, including credential issuance, discovery documents, revocation checks, TOFU key pinning, delegation chains, and mutual authentication across Rust, JavaScript, and Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External AgentPin packages may not come from the intended maintainer or may drift over time. <br>
Mitigation: Verify package provenance before installation and pin dependency versions. <br>
Risk: Generated private keys or credentials could be exposed if copied into source control or logs. <br>
Mitigation: Keep private keys out of source control, protect generated credentials, and use short-lived least-privilege credentials. <br>
Risk: TOFU pins, trust bundles, or delegated trust chains may preserve outdated or unintended trust decisions. <br>
Mitigation: Review, rotate, and reset TOFU pins or trust bundles through an explicit operational process. <br>


## Reference(s): <br>
- [AgentPin on ClawHub](https://clawhub.ai/jaschadub/agentpin) <br>
- [AgentPin README](https://github.com/ThirdKeyAI/agentpin/blob/main/README.md) <br>
- [AgentPin Technical Specification](https://github.com/ThirdKeyAI/agentpin/blob/main/AGENTPIN_TECHNICAL_SPECIFICATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code examples, JSON snippets, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may involve package installation, key generation, credential issuance, endpoint configuration, and verification workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

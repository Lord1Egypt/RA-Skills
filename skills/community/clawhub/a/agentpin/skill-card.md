## Description:

AgentPin helps AI assistants use domain-anchored cryptographic identity verification with ES256 JWTs, TOFU key pinning, revocation checks, and delegation chain validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaschadub](https://clawhub.ai/user/jaschadub)

### License/Terms of Use:


## Use Case:

Developers and engineers use AgentPin to add and verify cryptographic identity for AI agents across Rust, JavaScript, and Python implementations, including discovery, credential issuance, revocation, delegation, and offline trust bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides use of external npm and PyPI SDK packages.

Mitigation: Verify package identity, pin dependency versions for production or sensitive projects, and review packages through the normal supply-chain process before deployment.

Risk: Agent credentials and private keys are security-sensitive materials.

Mitigation: Store private keys and issued credentials only in appropriately protected project locations and rotate or revoke credentials when exposure is suspected.

## Reference(s):

- [AgentPin ClawHub skill page](https://clawhub.ai/jaschadub/skills/agentpin)
- [AgentPin README](https://github.com/ThirdKeyAI/agentpin/blob/main/README.md)
- [AgentPin Technical Specification](https://github.com/ThirdKeyAI/agentpin/blob/main/AGENTPIN_TECHNICAL_SPECIFICATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, API examples, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

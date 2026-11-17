## Description:

Secure key management for AI agents. Use when handling private keys, API secrets, wallet credentials, or when building systems that need agent-controlled funds. Covers secure storage, session keys, leak prevention, prompt injection defense, and MetaMask Delegation Framework integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zscole](https://clawhub.ai/user/zscole)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide AI agents that handle secrets, wallet credentials, delegated access, and agent-controlled funds. It focuses on secure storage, prompt-injection defense, output sanitization, session keys, and on-chain delegation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable wallet and secret-management examples may be unsafe if used directly with real funds or credentials.

Mitigation: Require human security review and hardening before production use.

Risk: Broad vault or session-key access can expose sensitive credentials or enable excessive wallet authority.

Mitigation: Use tightly scoped vault permissions, short-lived session keys, explicit spending limits, and transaction review.

Risk: Weak confirmation or delegation patterns can allow unauthorized actions.

Mitigation: Use strong random confirmation tokens bound to the user, session, and transaction details, and fully constrain delegation caveats.

Risk: Shell-based examples can introduce command execution risk when adapted into agent workflows.

Mitigation: Prefer non-shell command execution and review all command construction before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zscole/skills/bagman)
- [Delegation Framework Integration](references/delegation-framework.md)
- [Leak Prevention for Agent Secrets](references/leak-prevention.md)
- [Prompt Injection Defense for Agent Key Operations](references/prompt-injection-defense.md)
- [Secure Storage Patterns for Agent Secrets](references/secure-storage.md)
- [Session Keys for Agent Wallet Access](references/session-keys.md)
- [MetaMask Delegation Framework Deployments](https://github.com/MetaMask/delegation-framework/blob/main/documents/Deployments.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill requiring review before using copyable examples with real credentials or funds.]

## Skill Version(s):

2.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

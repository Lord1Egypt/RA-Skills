## Description:

Zero-knowledge secrets management via PassBox for storing, retrieving, rotating, and injecting credentials securely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paparusi](https://clawhub.ai/user/paparusi)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use A2A Vault to manage API keys, tokens, and environment credentials with client-side encryption. The skill supports vault and environment workflows, .env import and comparison, rotation, and credential injection into trusted tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external plugin that handles highly sensitive credentials.

Mitigation: Install only if A2A Corp and the @a2a/openclaw-plugin package source are trusted, and verify the package version before use.

Risk: .env imports, secret deletion, rotation, and environment promotion can change or expose operational credentials if invoked with the wrong vault, environment, or key names.

Mitigation: Review the .env keys and confirm vault, environment, and key names before importing, deleting, rotating, or promoting secrets.

Risk: Injected secrets can be exposed by downstream tools that log, forward, or persist inputs unexpectedly.

Mitigation: Inject secrets only into trusted tools after checking their logging and data-handling behavior.

## Reference(s):

- [A2A Vault ClawHub skill page](https://clawhub.ai/paparusi/skills/a2a-vault)
- [paparusi publisher profile](https://clawhub.ai/user/paparusi)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to use PassBox/OpenClaw plugin tools for secret storage, retrieval, import, deletion, rotation, and injection.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

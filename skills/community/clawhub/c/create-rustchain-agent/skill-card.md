## Description:

Scaffolds a runnable RustChain agent with an Ed25519 wallet, MCP wiring, node health checks, and a First-Light bounty claim path in one command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold a local RustChain-participating agent project with wallet material, a runnable agent script, editor MCP configuration, and onboarding notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold creates a plaintext wallet containing private key material.

Mitigation: Protect the generated wallet file, keep it out of version control, and use the scaffold only in environments where local wallet generation is acceptable.

Risk: Generated MCP wiring points tooling at the wallet path and may execute unpinned package versions.

Mitigation: Review .mcp.json before enabling it and pin exact versions of create-rustchain-agent and rustchain-mcp where possible.

Risk: The --register option and custom --node values can perform network operations against a selected RustChain node.

Mitigation: Use trusted node URLs, prefer testnet endpoints during evaluation, and avoid running scaffold commands copied from untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottcjn/skills/create-rustchain-agent)
- [RustChain](https://rustchain.org)
- [Project repository](https://github.com/Scottcjn/create-rustchain-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and inline shell commands describing generated files and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local scaffold files including wallet.json, agent.py, .mcp.json, README.md, and .gitignore; optional registration performs a network write.]

## Skill Version(s):

0.1.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

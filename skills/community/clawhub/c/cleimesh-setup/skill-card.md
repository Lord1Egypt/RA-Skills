## Description:

Put an AI agent's file work behind CleiMesh, so a prompt injection in an email or web page cannot read your keys or write where it wants, and every call leaves a signed receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cleitonaugusto](https://clawhub.ai/user/cleitonaugusto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to configure CleiMesh file access for supported agents, review setup plans, check that calls are routed through CleiMesh, and respond to refused writes or paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup downloads and runs an external installer, and this review does not verify the downloaded binary's security guarantees.

Mitigation: Review and verify the installer before running it; inspect the setup dry run and have the user run system-changing commands.

Risk: Setup creates a persistent service and disables the agent's native tools, which can affect its operation and access.

Mitigation: Inspect the dry-run plan, grant only narrow folders, and test with noncritical data first.

Risk: The publisher describes CleiMesh as alpha software.

Mitigation: Test with noncritical data first.

## Reference(s):

- [CleiMesh project](https://github.com/cleitonaugusto/cleimesh)
- [CleiMesh threat model](https://github.com/cleitonaugusto/cleimesh/blob/main/docs/threat-model.md)
- [CleiMesh alpha status](https://github.com/NVIDIA/OpenShell/discussions/4811)
- [CleiMesh Setup on ClawHub](https://clawhub.ai/cleitonaugusto/skills/cleimesh-setup)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands that change the system are prepared for the user to review and run.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

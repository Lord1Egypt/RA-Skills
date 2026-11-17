## Description:

Docker Mirror helps agents pull Docker images by trying Docker Hub first, then configured mirror registries when pulls fail in network-restricted Linux environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitsudog](https://clawhub.ai/user/kitsudog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when Docker image pulls fail or time out and they need an agent to route pull attempts through configured mirror registries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can execute unsafe shell input when handling Docker arguments.

Mitigation: Review the skill before installation, avoid untrusted image names or arguments, and do not use the wrapper for arbitrary Docker commands until the sg -c argument handling is fixed.

Risk: Retagging images pulled from third-party mirrors can hide their mirror provenance.

Mitigation: Use the skill only in environments where the configured mirrors are trusted, and prefer digest-pinned images when possible.

Risk: Docker access can affect host-adjacent state.

Mitigation: Run the skill only where Docker access is appropriate for the agent and operator-controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kitsudog/skills/docker-mirror)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on Docker, sg, and trust in the configured mirror registries.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

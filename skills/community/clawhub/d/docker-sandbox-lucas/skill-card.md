## Description:

Create and manage Docker sandboxed VM environments for safe agent execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasseeley](https://clawhub.ai/user/lucasseeley)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, run, restrict, inspect, and clean up Docker Desktop sandbox environments for agent execution, package exploration, destructive testing, and reproducible experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands run inside a sandbox can still modify mounted project files or saved sandbox state.

Mitigation: Use a disposable or backed-up workspace before running untrusted code, and review file changes before preserving or reusing sandbox state.

Risk: Network allowlists or proxy bypass settings may permit unexpected outbound access.

Mitigation: Start with a deny-by-default network policy and allow only the hosts required for the task.

Risk: Reset and remove commands can destroy sandbox state.

Mitigation: Confirm the target sandbox and save any required state before running reset or remove commands.

## Reference(s):

- [Docker Desktop Sandbox Documentation](https://docs.docker.com/desktop/features/sandbox/)
- [ClawHub Skill Page](https://clawhub.ai/lucasseeley/skills/docker-sandbox-lucas)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker Desktop 4.49+ with the docker sandbox plugin.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

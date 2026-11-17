## Description:

Docker安全沙箱环境，支持隔离运行与基础资源限制，适合代码测试。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create Docker-based sandbox environments for running untrusted code, testing container images, and performing isolated development experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to run local Docker and shell commands, which can affect the host environment if commands or mounts are unsafe.

Mitigation: Use an isolated workspace without secrets, review each command before execution, and avoid writable host mounts when running untrusted code.

Risk: Security evidence reports broad and partly inconsistent command-execution instructions.

Mitigation: Clarify intended API and network behavior before processing private code or data, and apply the server-provided review guidance before installation.

Risk: Docker isolation does not fully protect against kernel-level or advanced container escape threats.

Mitigation: Use stronger isolation such as a dedicated virtual machine for highly sensitive workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docker-sandbox-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Docker sandbox setup and execution guidance, including status-oriented command output expectations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

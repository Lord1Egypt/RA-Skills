## Description:

Distributed Inference helps agents coordinate local Ollama inference across macOS, Linux, and Windows nodes using HTTP and mDNS discovery, multi-signal routing, capacity learning, and context-aware model placement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, operate, query, and troubleshoot a self-hosted distributed-inference coordinator and node agents for heterogeneous local Ollama machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model pull, delete, and auto-pull actions can change remote nodes and transfer large model files.

Mitigation: Require explicit user approval before pull, delete, or auto-pull operations and confirm the target node and model name before execution.

Risk: The local dashboard and API can expose coordinator controls if bound to an untrusted interface.

Mitigation: Bind the dashboard and API only to trusted interfaces and run the coordinator as an unprivileged user in an isolated environment.

Risk: Installing an unpinned package can introduce unexpected code changes into the local inference environment.

Mitigation: Pin or verify the ollama-herd package version before installation or deployment.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/twinsgeeks/skills/distributed-inference)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)
- [ollama-herd project repository](https://github.com/geeks-accelerator/ollama-herd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, curl, and SQL command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local HTTP API endpoints, SQLite inspection commands, and operational constraints for model lifecycle actions.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

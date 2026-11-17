## Description:

Cuda Ollama helps agents route Ollama LLM inference across NVIDIA CUDA GPU fleets with load-aware scoring, vRAM-aware fallback, auto-retry, monitoring, and OpenAI-compatible endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate an Ollama router across multiple NVIDIA CUDA GPU machines. It provides commands, API examples, monitoring endpoints, and configuration guidance for local fleet inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the Ollama router package changes the local execution environment and starts local router or node services.

Mitigation: Install in a virtual environment or low-privilege account, review the package source, and pin a trusted version before use.

Risk: The Linux systemd commands can change the host Ollama service configuration.

Mitigation: Run those commands only when the operator intentionally wants to change the host Ollama service and has reviewed the service override.

Risk: Model downloads can consume substantial storage and model deletion can remove local assets.

Mitigation: Require explicit user confirmation for downloads and deletions, and keep automatic pulls disabled unless intentionally opted in.

## Reference(s):

- [Cuda Ollama ClawHub Skill](https://clawhub.ai/twinsgeeks/skills/cuda-ollama)
- [Ollama Herd GitHub Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama Herd PyPI Package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, curl, and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local service commands, API request examples, monitoring endpoints, and safety guardrails for model operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

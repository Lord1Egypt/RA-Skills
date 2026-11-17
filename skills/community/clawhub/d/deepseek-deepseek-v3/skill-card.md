## Description:

DeepSeek models on your local fleet - DeepSeek-V3, DeepSeek-V3.2, DeepSeek-R1, and DeepSeek-Coder routed across multiple devices via Ollama Herd, with 7-signal scoring to pick the best machine for each request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate DeepSeek models on local Apple Silicon or Linux machines through an Ollama Herd fleet. It helps agents provide setup commands, API examples, hardware guidance, monitoring details, and operational guardrails for local model routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running local fleet software with elevated privileges can expand the impact of a compromised dependency or misconfiguration.

Mitigation: Install in a virtual environment where possible, avoid sudo, and consider pinning or verifying the ollama-herd package before use.

Risk: Prompts, audio, and generated outputs may be visible to machines participating in the local fleet.

Mitigation: Only add trusted machines to the fleet and treat all participating devices as able to access routed request data.

Risk: Large DeepSeek model downloads can consume substantial disk, memory, and network resources.

Mitigation: Require user confirmation before pulling or deleting models, and suggest smaller variants when available memory is insufficient.

Risk: Changing fleet manager files can disrupt routing, logging, or latency tracking.

Mitigation: Do not delete or modify files in ~/.fleet-manager/ unless the user explicitly asks for that change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/deepseek-deepseek-v3)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, Python, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup steps, model selection guidance, API examples, dashboard endpoint details, and guardrails for model downloads and fleet configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Apple Silicon AI helps agents guide users through running LLMs, image generation, speech-to-text, and embeddings across Apple Silicon Macs as a local AI fleet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate local AI inference across Apple Silicon Macs, including routing requests for chat, image generation, speech-to-text, embeddings, and fleet monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing the unpinned ollama-herd package with pip.

Mitigation: Use a virtual environment and pin or verify the package version before installing, especially for multi-Mac deployments.

Risk: The referenced tool starts a local HTTP service on port 11435 and discovers nodes on the local network.

Mitigation: Run it only on trusted local networks and review host firewall exposure before deployment.

Risk: The tool writes local logs and routing metrics under ~/.fleet-manager.

Mitigation: Review retention and access expectations for ~/.fleet-manager/latency.db and ~/.fleet-manager/logs/herd.jsonl before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/apple-silicon-ai)
- [ollama-herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Troubleshooting](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline bash, Python, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup steps, endpoint examples, hardware recommendations, monitoring commands, and guardrails.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

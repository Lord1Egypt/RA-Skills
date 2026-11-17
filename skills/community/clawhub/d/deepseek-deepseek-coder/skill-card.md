## Description:

DeepSeek DeepSeek-Coder helps agents route DeepSeek-V3, DeepSeek-R1, and DeepSeek-Coder requests across a local Ollama Herd fleet on macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and call local DeepSeek models through an Ollama Herd fleet router, including OpenAI-compatible and Ollama API examples. It is intended for local multi-device model routing, monitoring, and model-size selection based on available memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a consent gap around automatic large model downloads, and DeepSeek variants can require substantial storage and memory.

Mitigation: Verify the ollama-herd package and version, confirm whether auto_pull is enabled, and require explicit approval before model downloads or deletions.

Risk: The security summary notes broader capabilities than the DeepSeek-focused framing suggests, including image generation, speech-to-text, embeddings, and routing for other local models.

Mitigation: Review enabled endpoints and local service exposure before use, and limit operation to the capabilities the deployment actually needs.

Risk: The guidance recommends care when running a third-party local model router and node service.

Mitigation: Use an isolated environment where practical, review configuration files under ~/.fleet-manager before changes, and avoid modifying or deleting fleet-manager data without explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/deepseek-deepseek-coder)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, Python, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local endpoint examples, hardware sizing guidance, and guardrails for model downloads and deletion.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

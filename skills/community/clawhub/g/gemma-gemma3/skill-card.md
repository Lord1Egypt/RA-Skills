## Description:

Gemma 3 by Google - run Gemma 3 models across a local device fleet with Ollama Herd routing on macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install and operate Ollama Herd, route Gemma 3 requests across a local device fleet, and call the router through OpenAI-compatible or Ollama-compatible APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed tool may send daily usage telemetry outside the user's network by default.

Mitigation: Set FLEET_NODE_TELEMETRY=false before first start when telemetry is not desired.

Risk: Installing an unpinned package can change behavior between runs.

Mitigation: Review the Ollama Herd package before installation and pin a specific version or verify package hashes where possible.

Risk: The router and node processes can access local fleet configuration and logs.

Mitigation: Run the tool in an isolated non-admin environment and avoid deleting or modifying files under ~/.fleet-manager/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/gemma-gemma3)
- [Ollama Herd GitHub repository](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama Herd PyPI package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes local service endpoints, model names, hardware recommendations, and guardrails for model pulls and deletion.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Set up and maintain an NVIDIA DGX Spark (GB10 Blackwell, 128GB unified memory) as a local LLM inference server running vLLM + LiteLLM + OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmy-hernandez](https://clawhub.ai/user/jimmy-hernandez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, and troubleshoot a DGX Spark as a private local LLM inference server with vLLM, LiteLLM routing, OpenClaw client configuration, and Tailscale remote access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide asks users to install packages and run external installers or source builds, which can introduce supply-chain risk or create a broken Python environment if artifacts drift.

Mitigation: Review and adapt commands before installing, prefer verified package-manager installs or pinned artifacts, pin Python dependency versions, and verify model code before using trusted-code loading.

Risk: The setup exposes a persistent inference service through LiteLLM and Tailscale, which can allow unintended access if keys, devices, or network scope are too broad.

Mitigation: Run services under least privilege and restrict Tailscale and LiteLLM access to intended users and devices.

## Reference(s):

- [LiteLLM Config Template](references/litellm-config-template.yaml)
- [DGX Spark vLLM Troubleshooting](references/troubleshooting.md)
- [Triton GitHub Repository](https://github.com/triton-lang/triton.git)
- [vLLM GitHub Repository](https://github.com/vllm-project/vllm.git)
- [PyTorch CUDA 13.0 Package Index](https://download.pytorch.org/whl/cu130)
- [Tailscale Install Script](https://tailscale.com/install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, verification, service configuration, client configuration, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

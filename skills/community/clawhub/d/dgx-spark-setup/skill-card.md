## Description: <br>
Set up and maintain an NVIDIA DGX Spark (GB10 Blackwell, 128GB unified memory) as a local LLM inference server running vLLM + LiteLLM + OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmy-hernandez](https://clawhub.ai/user/jimmy-hernandez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure a DGX Spark as a private local LLM inference server with vLLM, LiteLLM, OpenClaw, and Tailscale access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running vLLM with trusted remote model code can execute model-provided code. <br>
Mitigation: Use trusted model files and review the model source before enabling trust-remote-code. <br>
Risk: Installer commands fetched with curl can change over time or install unexpected software. <br>
Mitigation: Review installer scripts before execution and run them only from trusted sources. <br>
Risk: LiteLLM auto-start and Tailscale enrollment expose a persistent model-serving endpoint. <br>
Mitigation: Confirm the service should auto-start, use strong LiteLLM virtual keys, and approve only the intended machine in Tailscale. <br>


## Reference(s): <br>
- [LiteLLM config template](references/litellm-config-template.yaml) <br>
- [DGX Spark vLLM Troubleshooting](references/troubleshooting.md) <br>
- [Triton repository](https://github.com/triton-lang/triton.git) <br>
- [vLLM repository](https://github.com/vllm-project/vllm.git) <br>
- [PyTorch CUDA 13.0 package index](https://download.pytorch.org/whl/cu130) <br>
- [Tailscale installer](https://tailscale.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup commands, configuration snippets, and troubleshooting guidance for the DGX Spark model-serving stack.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

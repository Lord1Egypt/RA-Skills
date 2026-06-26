## Description: <br>
CUDA Ollama routes Ollama LLM inference across NVIDIA GPUs with automatic CUDA load balancing, 7-signal scoring, vRAM-aware fallback, and auto-retry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and operate an Ollama inference router across local NVIDIA CUDA GPU machines. It helps route requests, monitor fleet health, and apply safe operational controls for model downloads and deletions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the referenced router package from public package sources could introduce supply-chain risk. <br>
Mitigation: Verify the ollama-herd PyPI package and linked GitHub project before installation. <br>
Risk: A local inference router may expose GPU-backed model endpoints to unintended hosts if network access is broad. <br>
Mitigation: Run the router only on trusted machines and scope API or firewall access to intended hosts. <br>
Risk: Systemd or Windows environment changes can alter local Ollama behavior across sessions. <br>
Mitigation: Review sudo, systemd, and Windows environment changes before applying them. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/twinsgeeks/cuda-ollama) <br>
- [Ollama Herd GitHub repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd PyPI package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, curl, and PowerShell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no hidden code or credential collection reported by ClawScan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

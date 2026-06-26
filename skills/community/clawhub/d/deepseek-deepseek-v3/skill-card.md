## Description: <br>
DeepSeek models on your local fleet - DeepSeek-V3, DeepSeek-V3.2, DeepSeek-R1, DeepSeek-Coder routed across multiple devices via Ollama Herd, with 7-signal scoring to pick the best machine for each request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and route DeepSeek model requests across local Apple Silicon or Linux devices through Ollama Herd. It helps agents provide local-model setup guidance, API examples, hardware fit guidance, and operational guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeepSeek model downloads can be very large and may consume significant disk space, bandwidth, and memory. <br>
Mitigation: Confirm the exact model and size with the user before pulling models, and suggest smaller variants when available memory is insufficient. <br>
Risk: Local model services may bind to localhost or the LAN and expose model endpoints beyond the intended machine. <br>
Mitigation: Review the service bind address and network exposure before starting the router or node services. <br>
Risk: Fleet configuration and logs under ~/.fleet-manager may affect local routing behavior. <br>
Mitigation: Avoid deleting or modifying ~/.fleet-manager paths unless the user explicitly intends to manage the fleet configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/deepseek-deepseek-v3) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd PyPI package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup steps, model selection guidance, API examples, dashboard references, and operational guardrails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

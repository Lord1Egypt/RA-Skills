## Description: <br>
Configure, run, and troubleshoot Xrouter, an OpenAI-compatible LLM router that uses a hardware-aware classifier to route requests across local and cloud model providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pathemata-mathemata](https://clawhub.ai/user/pathemata-mathemata) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to set up an inference router, configure provider routes, run local or cloud-backed model endpoints, and inspect routing behavior and token usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented router defaults may expose a provider-backed chat proxy and usage dashboard. <br>
Mitigation: Bind HOST to localhost unless remote access is intentional, set ROUTER_API_KEY, and protect .env and upstreams.json. <br>
Risk: Prompts routed to cloud providers may be subject to provider retention or logging practices. <br>
Mitigation: Avoid routing sensitive prompts to cloud providers unless the provider's handling practices are trusted. <br>
Risk: Running an npm project from an untrusted source can execute code in the local environment. <br>
Mitigation: Review the source repository before installing dependencies or running npm commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pathemata-mathemata/clawhub-skill-2) <br>
- [Ollama Quickstart](https://ollama.readthedocs.io/en/quickstart/) <br>
- [vLLM OpenAI-Compatible Server](https://docs.vllm.ai/en/stable/serving/openai_compatible_server/) <br>
- [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) <br>
- [trtllm-serve](https://nvidia.github.io/TensorRT-LLM/1.0.0rc2/commands/trtllm-serve.html) <br>
- [llama.cpp](https://github.com/ggml-org/llama.cpp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, configuration keys, and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes router setup steps, provider configuration guidance, environment variables, and local service endpoints.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

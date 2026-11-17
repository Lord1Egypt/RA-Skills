## Description:

Configures, runs, and troubleshoots Xrouter, an OpenAI-compatible LLM routing proxy that uses a hardware-aware classifier to route requests across local and cloud providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pathemata-mathemata](https://clawhub.ai/user/pathemata-mathemata)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure an LLM routing proxy, connect local and cloud providers, test OpenAI-compatible chat requests, and inspect routing and token usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be forwarded to the configured local or cloud providers.

Mitigation: Configure only approved providers and avoid sending sensitive data to providers that have not been reviewed.

Risk: Provider API keys may be stored in local configuration files.

Mitigation: Keep .env and upstreams.json out of source control and restrict local file access.

Risk: The router may be exposed beyond localhost if bound to a broad network interface.

Mitigation: Bind the router only to trusted interfaces and require a router API key when it is reachable outside localhost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pathemata-mathemata/skills/clawhub-skill-2)
- [Ollama Quickstart](https://ollama.readthedocs.io/en/quickstart/)
- [vLLM OpenAI-Compatible Server](https://docs.vllm.ai/en/stable/serving/openai_compatible_server/)
- [NVIDIA TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)
- [TensorRT-LLM trtllm-serve](https://nvidia.github.io/TensorRT-LLM/1.0.0rc2/commands/trtllm-serve.html)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local service URLs, environment variables, provider settings, and request examples.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

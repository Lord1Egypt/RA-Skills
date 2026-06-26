## Description: <br>
Route OpenClaw chats to top Chinese LLMs with smart model selection, auto-fallback, cost tracking, and unified OpenAI-compatible API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xdd-xund](https://clawhub.ai/user/Xdd-xund) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure and route conversations to Chinese LLM providers, compare available models, receive task-based recommendations, and test provider connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and responses may be sent to configured third-party LLM providers. <br>
Mitigation: Use provider endpoints and data policies appropriate for the workload, and avoid sending sensitive or regulated data unless those providers are approved for that use. <br>
Risk: Provider API keys may be stored in a local configuration file. <br>
Mitigation: Restrict access to the configuration file and prefer low-quota, revocable API keys or environment-based secret management. <br>
Risk: Misconfigured or untrusted provider endpoints could expose prompts or credentials. <br>
Mitigation: Use trusted HTTPS endpoints and review provider base URLs before routing requests. <br>


## Reference(s): <br>
- [Chinese LLM API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Xdd-xund/chinese-llm-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces model recommendations, provider status, connectivity test output, and OpenAI-compatible chat-completion routing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

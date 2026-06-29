## Description: <br>
Helps developers choose, configure, and operate an OpenAI-compatible gateway that routes requests across Chinese AI API providers such as MiMo, DeepSeek, Qwen, GLM, and DashScope with priority fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare domestic Chinese AI API providers, obtain setup guidance, and generate OpenAI-compatible gateway configuration or sample code for chat, embeddings, image generation, and fallback routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API keys may be routed to third-party AI providers. <br>
Mitigation: Avoid sending secrets or regulated data, use environment variables or test keys with spending limits, and review each provider's terms before use. <br>
Risk: Fallback routing can send a request to a different provider than the user expected. <br>
Mitigation: Disable fallback or pin a single provider for sensitive workloads. <br>
Risk: Running the gateway on a public interface can expose the proxy to unauthenticated callers. <br>
Mitigation: Run it on localhost or behind authentication, firewall rules, and rate limits before exposing it beyond a trusted network. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qqyougitcom/china-api-gateway) <br>
- [中国AI API统一网关 - 详细内容](artifact/references/details.md) <br>
- [中国AI平台注册与API获取指南](artifact/references/platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API examples, shell commands, YAML configuration, and Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider recommendations, API key setup steps, gateway configuration, health checks, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

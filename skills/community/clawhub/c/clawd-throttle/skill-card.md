## Description: <br>
Routes LLM requests to the cheapest capable model across 8 providers (Anthropic, Google, OpenAI, DeepSeek, xAI, Moonshot, Mistral, Ollama) and 25+ models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liekzejaws](https://clawhub.ai/user/liekzejaws) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Clawd Throttle to classify prompt complexity, route LLM requests across configured providers, and inspect routing or cost statistics from an MCP server or local HTTP proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional HTTP proxy mode can allow unauthenticated callers to use configured LLM provider accounts if exposed. <br>
Mitigation: Run proxy mode only on trusted machines and networks, prefer localhost-only access, and add access controls before exposing the port. <br>
Risk: Prompts are sent to whichever external LLM providers the user configures. <br>
Mitigation: Configure only approved providers and install the skill only when provider-side prompt processing is acceptable. <br>
Risk: Administrative tools can reveal routing setup or persistently change routing behavior. <br>
Mitigation: Limit access to get_config and set_mode to trusted users and protect the local configuration directory. <br>


## Reference(s): <br>
- [Clawd Throttle ClawHub Page](https://clawhub.ai/liekzejaws/clawd-throttle) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Project Homepage](https://github.com/liekzejaws/clawd-throttle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Configuration, Shell commands, Guidance] <br>
**Output Format:** [MCP tool responses, HTTP proxy responses, JSON routing metadata, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model, complexity tier, classifier score, request ID, cost statistics, and configuration summaries with keys redacted.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

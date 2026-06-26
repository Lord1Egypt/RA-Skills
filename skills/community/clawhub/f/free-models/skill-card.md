## Description: <br>
Discover and select free or low-cost AI models from OpenRouter optimized for agents with filtering by price, context, provider, and capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to discover OpenRouter models that fit cost, context-window, provider, and simple capability requirements before selecting a model for OpenClaw or another agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI requires an OpenRouter API key even though the current model-list request does not need or transmit it. <br>
Mitigation: Use a limited OpenRouter key if setting one, and re-check future versions for credential-handling changes before running them. <br>
Risk: Model availability, pricing, and capability signals come from live OpenRouter data and can change over time. <br>
Mitigation: Review the selected model and current pricing in OpenRouter before using it in a production agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qidu/free-models) <br>
- [OpenRouter Models](https://openrouter.ai/models) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter API keys](https://openrouter.ai/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with JavaScript examples, shell commands, and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches live OpenRouter model data and filters model listings by price, context length, provider, name, and simple capability hints.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

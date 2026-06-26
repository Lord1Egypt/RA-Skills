## Description: <br>
Set up and use EZRouter, a unified LLM API gateway for Claude, GPT, and Gemini with provider-compatible endpoints and automatic failover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luntanwang](https://clawhub.ai/user/luntanwang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure EZRouter API keys, base URLs, SDK clients, and model-list checks for Claude, OpenAI-compatible, and Gemini-compatible workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, code, data, and API keys may be routed through a third-party LLM gateway. <br>
Mitigation: Review EZRouter retention, logging, security, and billing policies before using it with secrets, regulated data, customer data, or proprietary code. <br>
Risk: The EZRouter API key is a paid-account credential. <br>
Mitigation: Store it in environment variables or a secret manager, rotate it if exposed, and avoid committing it to configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luntanwang/ezrouter) <br>
- [EZRouter dashboard](https://openrouter.ezsite.ai) <br>
- [Claude-compatible API endpoint](https://openrouter.ezsite.ai/api/claude) <br>
- [OpenAI-compatible API endpoint](https://openrouter.ezsite.ai/api/openai/v1) <br>
- [Gemini-compatible API endpoint](https://openrouter.ezsite.ai/api/gemini) <br>
- [EZRouter model list endpoint](https://openrouter.ezsite.ai/api/model/list) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown with shell, JSON, Python, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for configuring third-party LLM gateway endpoints and API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

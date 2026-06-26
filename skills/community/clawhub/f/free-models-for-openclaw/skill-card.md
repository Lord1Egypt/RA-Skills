## Description: <br>
Discover, filter, and select free or low-cost AI models from OpenRouter for OpenClaw and other agent workflows based on context, price, and capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to discover free or low-cost OpenRouter models, filter them by provider, context window, price, and task requirements, and choose models for OpenClaw or other agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI asks for an OpenRouter API key even though the reviewed model-list request does not use it. <br>
Mitigation: Use a revocable OpenRouter key and avoid sharing the key in logs, prompts, or committed configuration. <br>
Risk: Model pricing and availability are fetched from OpenRouter at runtime and can change after publication. <br>
Mitigation: Review selected models and pricing before relying on the output in production or cost-sensitive workflows. <br>


## Reference(s): <br>
- [OpenRouter Models](https://openrouter.ai/models) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [ClawHub Skill Page](https://clawhub.ai/qidu/free-models-for-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with JavaScript and bash examples, plus text output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer for CLI execution; OpenRouter model availability and pricing are fetched live from the OpenRouter models API.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata; artifact package.json reports 0.2.1 and SKILL.md metadata reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

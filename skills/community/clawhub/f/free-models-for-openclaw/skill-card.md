## Description:

Discover, filter, and select free or low-cost AI models from OpenRouter for OpenClaw and other agent workflows based on context, price, and capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to discover and compare free or low-cost OpenRouter models for OpenClaw and other agent workflows. It supports filtering by provider, context length, price, model name, and task needs such as reasoning or vision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill asks for and reads an OpenRouter API key even though the current code does not use it for authenticated requests.

Mitigation: Review before installing, avoid providing a live OpenRouter API key unless needed, and prefer a version that removes or clearly scopes the key requirement.

Risk: Model availability, prices, and context lengths are fetched from OpenRouter at runtime and may change.

Mitigation: Verify selected model details against OpenRouter before relying on recommendations in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/free-models-for-openclaw)
- [OpenRouter models](https://openrouter.ai/models)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [OpenRouter API keys](https://openrouter.ai/settings/keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; exported functions return JavaScript objects and arrays.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output depends on current OpenRouter model metadata.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

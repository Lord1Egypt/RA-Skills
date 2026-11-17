## Description:

Discover and select free or low-cost AI models from OpenRouter for agent workflows, with filtering by price, context window, provider, and capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to find, filter, and select OpenRouter models that fit cost, context-length, provider, and capability requirements for OpenClaw or other agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release unnecessarily asks users to provide an OpenRouter API key even though the current model lookup code does not use it.

Mitigation: Review before installing, and do not paste or export a real OpenRouter API key for this CLI unless the package changes to require it and provides clear secret-handling guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qidu/skills/free-models)
- [OpenRouter](https://openrouter.ai)
- [OpenRouter Models](https://openrouter.ai/models)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model lists are fetched from OpenRouter at runtime and may change as provider pricing and availability change.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

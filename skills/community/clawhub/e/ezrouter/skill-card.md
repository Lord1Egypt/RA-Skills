## Description:

Set up and use EZRouter, a unified LLM API that provides one key for Claude, GPT, and Gemini with native API-compatible endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luntanwang](https://clawhub.ai/user/luntanwang)

### License/Terms of Use:


## Use Case:

Developers use this skill to configure EZRouter as a unified provider-compatible API for Claude, GPT, and Gemini in agent tools, SDKs, and command-line workflows. It provides setup guidance, base URLs, API examples, and model-listing commands for routing model calls through EZRouter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, code, private data, and the EZRouter API key are routed through a third-party intermediary service.

Mitigation: Use a dedicated EZRouter key, avoid sending sensitive code or private data unless the service's privacy and security posture is acceptable, and review terms before routing production model traffic through EZRouter.

## Reference(s):

- [EZRouter Dashboard](https://openrouter.ezsite.ai)
- [Claude API Endpoint](https://openrouter.ezsite.ai/api/claude)
- [OpenAI API Endpoint](https://openrouter.ezsite.ai/api/openai/v1)
- [Gemini API Endpoint](https://openrouter.ezsite.ai/api/gemini)
- [EZRouter Model List Endpoint](https://openrouter.ezsite.ai/api/model/list)
- [ClawHub Skill Page](https://clawhub.ai/luntanwang/skills/ezrouter)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash, JSON, Python, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; examples include API keys as placeholders and do not create files or execute code on their own.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

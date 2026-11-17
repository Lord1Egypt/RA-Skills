## Description:

Searches the web for real-time information with DashScope Qwen, including fresh results, site-restricted searches, citations, and optional images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreo992](https://clawhub.ai/user/oreo992)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to answer current-events, research, factual lookup, and visual reference requests by calling DashScope Qwen web search from an agent or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation can send user queries to DashScope without a clear privacy or consent boundary.

Mitigation: Review before installing where conversations may include secrets, personal data, customer data, or regulated information, and narrow activation rules so external search runs only when appropriate.

Risk: The skill requires a DashScope API key and the openai Python package at runtime.

Mitigation: Configure the API key only in a least-privileged runtime and prefer a pinned dependency or isolated environment.

## Reference(s):

- [DashScope](https://dashscope.aliyuncs.com/)
- [DashScope Console](https://dashscope.console.aliyun.com/)
- [OpenClaw](https://github.com/nicepkg/openclaw)
- [DashScope Web Search on ClawHub](https://clawhub.ai/oreo992/skills/dashscope-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown/text with numbered citations and optional Markdown image links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source lists, citation markers, and optional image references.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

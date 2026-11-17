## Description:

Connects MCP-compatible agents to ten Chinese model providers for text and multimodal requests, with health checks and usage reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers connect MCP-compatible agents to Chinese model providers for chat, image and video understanding, transcription, embeddings, reranking, and batch requests. They can also compare providers and generate health and usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media or text inputs are sent to configured model providers.

Mitigation: Use only providers approved for the data you submit.

Risk: API keys and locally stored prompts or results may be exposed if configuration or local data is accessible to others.

Mitigation: Prefer environment variables for API keys and protect local ~/.cn-model-gateway databases.

Risk: Optional report webhooks can send reports to an unintended destination.

Mitigation: Configure only trusted webhook URLs and review reports before enabling delivery.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fyniujin/skills/cn-model-gateway)
- [Provider error mapping](references/error_map.yaml)
- [DeepSeek platform](https://platform.deepseek.com/)

## Skill Output:

**Output Type(s):** [Text, Code, JSON tool responses, HTML reports]

**Output Format:** [Text or JSON responses, with optional local HTML health reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider-dependent answers; batch tasks can retain prompts and results locally.]

## Skill Version(s):

1.9.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use when generating or reasoning over text with Alibaba Cloud Model Studio Qwen flagship text models (`qwen3-max`, `qwen3.5-plus`, `qwen3.5-flash`, snapshots, and compatible open-source variants).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build text generation, reasoning, chat, tool-calling, and long-context workflows on Alibaba Cloud Model Studio Qwen models. It helps prepare normalized request payloads, choose model variants, and keep reproducible request examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generated outputs, or request payloads may contain secrets or regulated data sent to Alibaba Cloud Model Studio.

Mitigation: Confirm Alibaba Cloud Model Studio is an approved destination before use, avoid sending secrets or regulated data, and use a least-privilege DashScope API key.

Risk: Generated request and response files may be written to locations that are not appropriate for sensitive content.

Mitigation: Keep request and response files in a controlled output directory and avoid passing untrusted values to the helper script's --output option.

Risk: Dependency drift in the DashScope package can change runtime behavior.

Mitigation: Pin the DashScope package version when reproducible behavior is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-generation)
- [Model release and update notes](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Qwen text generation model list](https://help.aliyun.com/zh/model-studio/models)
- [Text generation overview](https://help.aliyun.com/zh/model-studio/text-generation)
- [OpenAI-compatible API](https://help.aliyun.com/zh/model-studio/openai-compatible)
- [Artifact reference sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API examples, and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create normalized request JSON files under output/aliyun-qwen-generation/requests/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

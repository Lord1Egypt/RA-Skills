## Description:

Sends a single user prompt to Alibaba Cloud DashScope through its OpenAI-compatible chat API for quick LLM checks, prompt experiments, and one-shot text generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhendong](https://clawhub.ai/user/pengzhendong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to send a simple single-turn chat request to DashScope models from an agent workflow or local CLI. It is suited for quick prompt testing and lightweight text generation when DashScope credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts passed through --message are sent to Alibaba Cloud DashScope.

Mitigation: Do not include secrets, regulated data, or proprietary text unless that use is approved for DashScope.

## Reference(s):

- [DashScope OpenAI-Compatible API Endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)
- [ClawHub Skill Page](https://clawhub.ai/pengzhendong/skills/dashscope-llm)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text response printed to stdout, with markdown guidance and shell command examples in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-turn response; no streaming, tool calling, structured output handling, or advanced retry management.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use DeepSeek V4 Flash and Pro from the command line for one-shot Q&A, thinking mode, and multi-turn chat through an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call DeepSeek V4 Flash or Pro from a terminal for Q&A, writing, coding, summaries, reasoning, and multi-turn chat. It is useful when an agent needs practical command examples, model selection guidance, or configuration steps for DeepSeek API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, system prompts, and chat history are sent to DeepSeek's remote API.

Mitigation: Avoid submitting secrets, regulated data, or sensitive internal content unless this use is approved.

Risk: The one-shot and chat scripts depend on the OpenAI Python SDK at runtime.

Mitigation: Pin the SDK dependency or run the scripts in a constrained environment for stronger supply-chain hygiene.

## Reference(s):

- [ClawHub Deepseek V4 Skill](https://clawhub.ai/jiajiaoy/skills/deepseek-v4)
- [DeepSeek API Documentation](https://api-docs.deepseek.com)
- [DeepSeek API Keys](https://platform.deepseek.com/api_keys)
- [DeepSeek Platform](https://platform.deepseek.com)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and streamed text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and DEEPSEEK_API_KEY; prompts, system prompts, and chat history are sent to DeepSeek's remote API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

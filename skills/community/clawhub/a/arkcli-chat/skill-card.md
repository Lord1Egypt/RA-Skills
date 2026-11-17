## Description:

arkcli +chat：通过数据面 Responses API 快速对话/推理，支持多模态、流式、多轮、临时 API Key/Base URL/Endpoint 执行与无副作用 dry-run。当用户给出 Endpoint 但未说明工作流时，先用 resources resolve 识别候选；已经出现 Responses API capability/access 错误时，只读用 models get 核对精确模型的 api_support，不重试真实调用。有明确产出形态的多模态理解走 arkcli-understand。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use arkcli +chat for text and multimodal conversations through the Responses API, including streaming, stored follow-up turns, tool use, and structured JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --store retains conversation data on the service.

Mitigation: Before installing, decide whether you accept that retention and use --store only when you agree to it.

Risk: The security scan had partial coverage because two referenced paths were unavailable.

Mitigation: Review those referenced files if they are supplied separately before relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jasonstarlight/skills/arkcli-chat)
- [+chat reference](references/arkcli-chat.md)
- [Caching, thinking, and expiration reference](references/caching-thinking.md)
- [Stored chat response commands reference](references/chat-meta.md)
- [Chat regression scenarios](references/evals.md)
- [Streaming events reference](references/stream-events.md)
- [Text formatting reference](references/text-format.md)
- [Tools reference](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Text or JSON responses; optional NDJSON streaming events, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include multiple modalities, streaming events, usage metadata, or tool-call data depending on the request.]

## Skill Version(s):

1.2.5 (source: artifact frontmatter; ClawHub release metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

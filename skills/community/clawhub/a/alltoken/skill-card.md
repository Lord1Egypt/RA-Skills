## Description:

Bootstrap a modular AllToken agent - chat, async image+video, model routing, OpenAI-compatible SDK. Works inside Hermes, OpenClaw, Claude Code, Codex CLI, OpenCode, or any runtime that loads SKILL.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alltoken-ai](https://clawhub.ai/user/alltoken-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scaffold TypeScript or Python projects that call AllToken for chat, async image generation, async video generation, model discovery, routing, and cost tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and media requests are sent to AllToken with an ALLTOKEN_API_KEY.

Mitigation: Use the skill only when that data sharing is acceptable, keep the API key in the environment, and avoid committing or hard-coding secrets.

Risk: The HTTP server example can expose chat history and paid API access if deployed unchanged.

Mitigation: Add authentication, per-user session ownership, rate limits, request validation, retention limits, and avoid returning full conversation history before any deployment.

Risk: Generated scaffold dependencies may drift or introduce supply-chain exposure.

Mitigation: Pin and review dependencies before running the scaffold in a real project.

## Reference(s):

- [AllToken ClawHub Skill Page](https://clawhub.ai/alltoken-ai/skills/alltoken)
- [AllToken Homepage](https://alltoken.ai)
- [AllToken API Overview](https://alltoken.ai/docs/apis/overview)
- [AllToken Chat Completions API](https://alltoken.ai/docs/apis/completions)
- [AllToken Image Generation API](https://alltoken.ai/docs/apis/image)
- [AllToken Video Generation API](https://alltoken.ai/docs/apis/video)
- [OpenAI TypeScript SDK](https://github.com/openai/openai-node)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Ink Terminal UI](https://github.com/vadimdemedes/ink)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline code blocks, shell commands, and generated project file contents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are project scaffolding guidance and source files; generated projects require ALLTOKEN_API_KEY and should be reviewed before deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

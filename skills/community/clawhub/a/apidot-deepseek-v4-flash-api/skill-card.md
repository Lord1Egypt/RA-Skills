## Description:

Use APIDot for DeepSeek V4 Flash API workflows, including OpenAI-compatible chat, 1M-token long-context reasoning, fast non-thinking responses, prompt-guided reasoning, code review, agent planning, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route APIDot DeepSeek V4 Flash API questions to current documentation, plan OpenAI-compatible chat integrations, handle long-context and streaming considerations, and keep API key handling server-side.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat this documentation router as a general code review or planning skill.

Mitigation: Use it only for APIDot DeepSeek V4 Flash API work and verify current APIDot docs before implementation decisions.

Risk: APIDOT_API_KEY or sensitive prompts, documents, request metadata, or generated responses could be exposed through unsafe logging or frontend code.

Mitigation: Keep API keys in backend secret storage, avoid exposing private data in public logs or client bundles, and treat prompts and outputs as sensitive unless explicitly cleared for sharing.

Risk: Model-specific fields, availability, limits, or commercial terms may change outside the artifact.

Mitigation: Consult the live APIDot model page and API docs before production rollout or copyable request construction.

## Reference(s):

- [APIDot Docs](https://apidot.ai/docs)
- [APIDot DeepSeek V4 Flash Model Page](https://apidot.ai/models/deepseek-v4-flash)
- [APIDot DeepSeek V4 Flash API Docs](https://apidot.ai/docs/deepseek-v4-flash)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Error Guidance](https://apidot.ai/docs/errors)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot DeepSeek V4 Flash Reference](references/api.md)
- [Publisher Profile](https://clawhub.ai/user/jiehao71727)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-deepseek-v4-flash-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with links, integration planning notes, code-oriented advice, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable files, automatic network calls, bundled API clients, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automatically escalates difficult or low-confidence tasks to Doubao, Qianwen, Kimi, or DeepSeek for proposed solutions and follow-up validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielwang20150225-source](https://clawhub.ai/user/danielwang20150225-source)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when they cannot confidently solve a task or when a proposed solution requires manual user work. It sends a structured prompt to prioritized third-party AI assistants, checks for responses, asks follow-up questions, and returns executable guidance to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task context may be sent to named third-party AI providers automatically.

Mitigation: Require explicit user approval and show the exact outbound prompt before sending sensitive or proprietary context.

Risk: The skill may use the user's logged-in accounts, sessions, or quotas when contacting external AI services.

Mitigation: Confirm account usage before provider access, avoid cookie or session handling where possible, and stop for login or captcha prompts.

Risk: AI replies may be saved to memory without enough consent or retention control.

Mitigation: Make memory retention opt-in and avoid storing sensitive prompts or responses unless the user approves.

Risk: Provider fallback and multi-turn polling can broaden disclosure beyond the first selected AI service.

Mitigation: Limit provider switching to approved services and ask again before forwarding the same task to another provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielwang20150225-source/skills/ask-ai-assistant)
- [Doubao](https://www.doubao.com)
- [Qianwen](https://qianwen.aliyun.com)
- [Kimi](https://kimi.moonshot.cn)
- [DeepSeek](https://www.deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with structured status markers and optional code or command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multi-turn AI responses, feasibility checks, execution notes, and final status labels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

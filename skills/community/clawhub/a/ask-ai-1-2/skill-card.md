## Description:

Automatically asks Doubao, Qianwen, Kimi, or DeepSeek for a concrete solution when the agent encounters a difficult problem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielwang20150225-source](https://clawhub.ai/user/danielwang20150225-source)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw agent users use this skill to route hard technical questions to third-party AI chat services, collect responses, and apply or summarize proposed solutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and context may be submitted to third-party AI services through persistent logged-in browser sessions.

Mitigation: Review and redact prompts before use; do not include secrets, regulated data, private source code, internal URLs, account details, or other sensitive data.

Risk: Model responses and execution details may be stored in agent memory.

Mitigation: Use only with information approved for retention, or change the skill to require opt-in memory storage.

Risk: The skill requires acting on third-party model advice without fresh user approval.

Mitigation: Require explicit user approval and human review before executing model-suggested commands, code changes, or operational steps.

Risk: Persistent logged-in browser profiles may reuse cookies and account access across sessions.

Mitigation: Use dedicated accounts with minimal access and clear or revoke sessions when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielwang20150225-source/skills/ask-ai-1-2)
- [Doubao chat](https://www.doubao.com/chat/)
- [Qianwen](https://qianwen.aliyun.com)
- [Kimi](https://kimi.moonshot.cn)
- [DeepSeek](https://www.deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or conversational text with command and code snippets when returned by the selected model]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single conversational stream with required status markers, response summaries, and follow-up decisions.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

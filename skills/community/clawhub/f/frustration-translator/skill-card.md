## Description:

Detect user frustration in prompts and translate charged or emotional language into clear, actionable instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recognize emotionally charged user messages, infer the underlying task from nearby conversation context, and respond with direct action. It is intended to reduce wasted context and misinterpretation when urgency or frustration obscures the actual request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage retaining conversation-derived details in a local frustration log, including sensitive user text or business context.

Mitigation: Remove or sanitize log entries, avoid verbatim user text and business details, and require explicit consent before retaining conversation-derived records.

Risk: The skill tells agents to move quickly and avoid extra caveats when users sound urgent, which could suppress normal clarification or safety checks.

Mitigation: Preserve required safety, privacy, and clarification behavior even when using the frustration score to prioritize concise action.

## Reference(s):

- [Frustration Log](references/frustration-log.md)
- [ClawHub Skill Page](https://clawhub.ai/dodge1218/skills/frustration-translator)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown guidance and concise natural-language response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local frustration-log entries when retention is enabled by the operating environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

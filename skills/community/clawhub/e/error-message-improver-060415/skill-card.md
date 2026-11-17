## Description:

Helps developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what to do next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and affected users use this skill to convert unclear error states into actionable messages, workflows, checklists, code changes, or support guidance. It is most useful when an error needs to state the failure, likely cause, next action, assumptions, and validation criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad debugging, support, or troubleshooting requests because its triggers are broad.

Mitigation: Invoke it explicitly for error-message work when possible and review whether the requested task is actually about improving an error message.

Risk: Generated messages or plans may be misleading if the original error context is incomplete.

Mitigation: Validate that the result explains what failed, why it failed, and what action to take next, and keep assumptions and remaining gaps visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/error-message-improver-060415)
- [Requirement Plan](artifact/references/requirement-plan.md)
- [Dify GitHub issue: undeployed Agent backend error](https://github.com/langgenius/dify/issues/39161)
- [Aether GitHub issue: verbose log levels](https://github.com/CluvexStudio/Aether/issues/39)
- [SegmentFault error-messages tag](https://segmentfault.com/t/error-messages)
- [Hacker News discussion: Ghostel.el](https://news.ycombinator.com/item?id=48905348)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text, optionally with code, shell commands, configuration snippets, checklists, or decision aids]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, risks, and follow-up work]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

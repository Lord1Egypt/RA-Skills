## Description:

Helps application developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to improve error-message clarity, troubleshooting guidance, and support workflows. It helps produce tailored artifacts such as rewritten messages, checklists, workflow guidance, analysis, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad debugging or support phrasing may cause the skill to activate for requests that are not specifically about improving user-facing error messages.

Mitigation: Use narrower invocation wording and confirm the requested outcome before applying the error-message workflow.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-070243)
- [Chatflow/Workflow Agent Node Issue](https://github.com/langgenius/dify/issues/39161)
- [Dart unawaited FutureOr Issue](https://github.com/dart-lang/sdk/issues/63818)
- [SegmentFault Error Messages Topic](https://segmentfault.com/t/error-messages)
- [Hacker News Ghostel.el Discussion](https://news.ycombinator.com/item?id=48905348)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown or plain text, with code snippets when implementation support is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, workflows, templates, assumptions, validation notes, and follow-up risks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

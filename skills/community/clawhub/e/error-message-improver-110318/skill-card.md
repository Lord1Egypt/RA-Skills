## Description:

Helps developers, support teams, SaaS operators, and users turn vague error messages into clearer guidance that explains what failed, why it failed, and what to do next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to rewrite or plan error-handling guidance so failures are easier to understand and troubleshoot. It supports practical workflows, checklists, analysis, code changes, and verification notes for clearer user-facing errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may invoke the skill for generic support or debugging requests where a general assistant response would be more appropriate.

Mitigation: Review and narrow activation phrases before deployment in agents that auto-invoke skills.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-110318)
- [Dify Agent Backend Error Issue](https://github.com/langgenius/dify/issues/39161)
- [Dart FutureOr Error Message Issue](https://github.com/dart-lang/sdk/issues/63818)
- [Medusa Migration Deadlock Error Issue](https://github.com/medusajs/medusa/issues/16011)
- [SegmentFault Error Messages Topic](https://segmentfault.com/t/error-messages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, checklists, and concise validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable workflows, assumptions, limitations, and follow-up work when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

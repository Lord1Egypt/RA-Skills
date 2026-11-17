## Description:

Helps developers, support teams, and SaaS operators rewrite vague error messages so they explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and SaaS operators use this skill to turn unclear error reports into actionable messages, workflows, checklists, templates, code changes, or troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad debugging, support, or productivity wording may cause the skill to be invoked outside error-message improvement tasks.

Mitigation: Invoke it explicitly when the goal is to improve error-message copy or troubleshooting-message guidance.

Risk: Generated error messages may still misstate root cause or next steps if the user provides incomplete technical context.

Mitigation: Review the proposed wording against logs, product behavior, and support policy before publishing it to users.

## Reference(s):

- [Error Message Improver ClawHub Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-080317)
- [Requirement Plan](references/requirement-plan.md)
- [Dify agent backend issue](https://github.com/langgenius/dify/issues/39161)
- [SegmentFault error-messages topic](https://segmentfault.com/t/error-messages)
- [Hacker News Ghostel.el discussion](https://news.ycombinator.com/item?id=48905348)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text guidance with optional code, commands, checklists, and templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; security evidence reports no code execution, credential access, persistence, or data exfiltration behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

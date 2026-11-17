## Description:

Helps developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what to do next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to rewrite, plan, or evaluate error-message improvements so troubleshooting output states the failure, likely cause, next action, assumptions, and validation criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit triggers may route generic support, debugging, or user-feedback requests to this skill when a more specific skill is intended.

Mitigation: Review trigger keywords and implicit-invocation policy before deployment in environments that require precise skill routing.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Improve error messages in config](https://github.com/yrn-dev/project-zero-1773324380/issues/126)
- [Error messages topic](https://segmentfault.com/t/error-messages)
- [Designing APIs for Agents](https://news.ycombinator.com/item?id=48929039)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, checklists, workflows, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, remaining risks, follow-up work, and locally executable implementation steps when relevant]

## Skill Version(s):

0.20260729.110214 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

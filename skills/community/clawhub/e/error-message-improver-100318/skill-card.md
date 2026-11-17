## Description:

Helps developers and support teams turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to improve error messages, debugging workflows, support responses, templates, checklists, and implementation guidance. It is intended to make troubleshooting outcomes clearer without requiring cloud-only tooling or specialized hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked more often than intended because it includes broad triggers such as support, debugging, troubleshooting, and work-productivity.

Mitigation: Review invocation settings before installation and prefer explicit invocation in environments where generic support or debugging requests should route to another workflow.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-100318)
- [Developer Onboarding Funnel Metrics with Dropoff Analysis](https://github.com/sethdford/shipwright/issues/746)
- [Replace manual config validation with zod](https://github.com/SchneiderDaniel/cheasee-pi/issues/1208)
- [What I had to unlearn as a perfectionist before I could ship](https://news.ycombinator.com/item?id=48774284)
- [You should not copy-paste errors into Claude Code](https://news.ycombinator.com/item?id=48727244)
- [Error Messages Topic](https://segmentfault.com/t/error-messages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include concise workflows, templates, checklists, analysis, implementation changes, validation notes, assumptions, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to rewrite, structure, or review error messages so troubleshooting guidance is actionable. It can produce tailored wording, workflows, checklists, analyses, code changes, scripts, or decision support for error-message improvement tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to appear for general debugging or support prompts.

Mitigation: Invoke it explicitly when the intended task is rewriting, structuring, or reviewing error messages.

Risk: Generated wording, workflows, scripts, or code changes may be misleading if the failure context or success criteria are incomplete.

Mitigation: Review the output against the target system behavior, stated assumptions, and validation criteria before deployment.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/error-message-improver-071732)
- [Classify prose/empty LLM generation output separately from architecture regressions](https://github.com/promptdriven/pdd/issues/1649)
- [Error message improvements](https://github.com/jump-dev/JuMP.jl/issues/4175)
- [Hung tool calls should be cancellable](https://github.com/anthropics/claude-code/issues/69372)
- [SegmentFault error-messages](https://segmentfault.com/t/error-messages)
- [Hacker News Typst 0.15.0 discussion](https://news.ycombinator.com/item?id=48545698)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, sometimes with code blocks or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include checklists, templates, analyses, code changes, scripts, and validation notes tailored to the user's error-message task.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

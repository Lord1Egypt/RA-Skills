## Description:

Helps users create clearer error messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to turn vague or unhelpful errors into actionable messages, troubleshooting workflows, checklists, code guidance, or decision support. It is intended to clarify context, assumptions, next steps, and verification criteria for debugging and support tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to be used for general support or debugging requests where a narrower skill or ordinary assistant behavior would fit better.

Mitigation: Confirm the user needs error-message improvement, troubleshooting guidance, or support workflow help before relying on the skill's workflow.

Risk: Generated error-message rewrites or troubleshooting guidance may be incomplete or misleading if the original error context is sparse.

Mitigation: State assumptions, preserve important diagnostic details, and validate the result against the user's success criteria before use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-005353)
- [Quality Grading Weights setting and option strategy quality calculation improvements](https://github.com/GeneBO98/tradetally/issues/352)
- [bug: generate ignores files with wildcards specified in config file](https://github.com/bennypowers/cem/issues/359)
- [upkeep plan for summer 2026](https://github.com/topepo/caret/issues/1418)
- [Bug: Silent catch blocks swallow errors without logging or actionable feedback](https://github.com/khanirfan18/finBoard/issues/211)
- [error-messages](https://segmentfault.com/t/error-messages)
- [Typst 0.15.0](https://news.ycombinator.com/item?id=48545698)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, command snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, required inputs, and any remaining follow-up work.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

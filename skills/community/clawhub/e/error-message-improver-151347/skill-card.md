## Description:

Helps developers, support teams, SaaS operators, and users turn vague error messages into clearer explanations that state what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to rewrite or plan clearer error messaging for troubleshooting, product feedback, support replies, and debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to activate for general debugging or support-writing requests.

Mitigation: Review or narrow invocation settings when broad automatic activation is not desired.

Risk: Suggested error-message changes may be incomplete or misleading if the user provides too little context.

Mitigation: State assumptions, ask only for materially missing information, and validate the result against the user's success criteria.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-151347)
- [Requirement Plan](references/requirement-plan.md)
- [Classify prose/empty LLM generation output separately from architecture regressions](https://github.com/promptdriven/pdd/issues/1649)
- [Endpoint Authoring with Better Autocomplete and Actionable Error Messages](https://github.com/VoidenHQ/voiden/issues/448)
- [Error message improvements](https://github.com/jump-dev/JuMP.jl/issues/4175)
- [error-messages](https://segmentfault.com/t/error-messages)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text with optional code snippets, checklists, workflows, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, limits, required inputs, and next-step notes when useful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

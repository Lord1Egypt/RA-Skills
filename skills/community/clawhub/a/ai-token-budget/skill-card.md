## Description:

TokenBudget helps an agent check token budgets before LLM calls, choose lower-cost models when budgets are tight, and report budget status to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenrl2006](https://clawhub.ai/user/wenrl2006)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add session-scoped token budget checks, cost estimates, model selection guidance, and user-facing budget reports to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic model downgrades may reduce response quality for budget-constrained tasks.

Mitigation: Treat model recommendations as guidance and let users confirm high-impact or deep-reasoning work before downgrading.

Risk: Budget enforcement can skip or block low-priority tasks when configured limits are reached.

Mitigation: Expose budget status and allow explicit user commands to adjust or temporarily disable budget limits for the current session.

Risk: The skill may recommend installing a TokenBroker gateway when local broker health checks are unavailable.

Mitigation: Verify the package source before running suggested install commands, as recommended by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenrl2006/skills/ai-token-budget)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and TypeScript helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-scoped budget configuration, token estimates, model recommendations, and optional budget warning text.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

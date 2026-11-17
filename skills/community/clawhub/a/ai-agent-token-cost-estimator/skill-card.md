## Description:

Estimate token usage and approximate API cost of AI agents by analyzing model choice, reasoning steps, tool use, context growth, and output size before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showmethemoney2023](https://clawhub.ai/user/showmethemoney2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI builders use this skill to estimate per-run token usage and API cost for agent workflows before deployment. It helps identify cost drivers and suggests practical ways to reduce token consumption and avoid unexpected bills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cost estimates may be inaccurate when model pricing, workflow steps, tool retries, context size, or output length differ from the assumptions provided.

Mitigation: Verify current pricing and compare estimates with runtime token limits, step limits, retry limits, budget monitoring, and observed usage before relying on them for production budgeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showmethemoney2023/skills/ai-agent-token-cost-estimator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style cost estimate with token ranges, cost ranges, cost drivers, and optimization suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rough planning estimates; current model pricing should be verified separately for production budgeting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

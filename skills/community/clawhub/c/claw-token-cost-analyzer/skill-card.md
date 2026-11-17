## Description:

Analyzes Claw AI workflows to estimate token usage and cost, identify runaway loop risk, and suggest optimizations before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showmethemoney2023](https://clawhub.ai/user/showmethemoney2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to review Claw workflows, prompts, or task descriptions for token usage, estimated cost per run, runaway-loop risk, and cost-control improvements before deploying automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cost estimates may be inaccurate if the supplied workflow, prompt, model pricing, or runtime behavior is incomplete or changes after review.

Mitigation: Treat estimates as advisory and validate them against actual model usage, current pricing, and production telemetry before relying on them for budgeting.

Risk: Workflow or prompt examples submitted for analysis may contain API keys, credentials, or confidential prompt text.

Mitigation: Avoid including secrets or confidential content unless it is necessary for the analysis, and redact sensitive values where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showmethemoney2023/skills/claw-token-cost-analyzer)
- [Publisher profile](https://clawhub.ai/user/showmethemoney2023)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with risk level, token estimate, cost estimate, issues detected, and optimization suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates are advisory and depend on the workflow, prompt, model pricing, and execution behavior supplied by the user.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

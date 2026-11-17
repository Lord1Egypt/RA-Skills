## Description:

Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivansslo](https://clawhub.ai/user/ivansslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to decide when independent debugging or implementation tasks should be delegated to parallel subagents and how to scope each agent prompt for reviewable integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel subagents may make conflicting or overlapping changes if tasks are not truly independent.

Mitigation: Dispatch only clearly independent scopes and check returned changes for file or behavior conflicts before integration.

Risk: Subagent outputs may include incorrect fixes, incomplete analysis, or misleading summaries.

Mitigation: Review each subagent result and run relevant tests before accepting or merging the changes.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/ivansslo/Supwrs/tree/main/skills/dispatching-parallel-agents)
- [ClawHub skill page](https://clawhub.ai/ivansslo/skills/dispatching-parallel-agents-3)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with structured examples and agent prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review returned subagent summaries and run tests before accepting changes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

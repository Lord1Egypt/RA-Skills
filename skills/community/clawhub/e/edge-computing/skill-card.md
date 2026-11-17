## Description:

Provides an edge computing workflow for deciding what runs at the edge versus origin and reviewing caching, data locality, security, platform limits, cost, and latency validation for CDN and edge worker deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to plan and review CDN and edge worker deployments, including workload fit, edge versus origin responsibilities, state strategy, tenant security, platform limits, cost, and regional rollout validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform-specific edge runtime limits, APIs, and security controls may differ from the general workflow.

Mitigation: Verify the target platform's documented limits, available APIs, and security controls before making production changes.

Risk: Incorrect edge versus origin placement can affect latency, cost, caching behavior, or fallback reliability.

Mitigation: Document origin responsibilities, platform limits, cost assumptions, fallback behavior, and canary validation before rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike47512/skills/edge-computing)
- [Publisher profile](https://clawhub.ai/user/mike47512)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with checklists and implementation review prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow; no embedded code, persistence, or tool execution is reported by the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

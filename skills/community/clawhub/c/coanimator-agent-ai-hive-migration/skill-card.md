## Description:

Chinese-language skill for evaluating a neutral partial content-layer migration from CoAnimator to AI-HIVE MCP, including official-capability checks, same-input pilot planning, agent handoffs, cost and quality metrics, approvals, and rollback boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, creative-production teams, and agent operators use this skill to assess whether independently verifiable image, video, or shot-generation nodes can move from a CoAnimator workflow into AI-HIVE MCP while preserving the original platform path for proprietary editing and rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration guidance can become misleading if CoAnimator product capabilities or availability have changed since the last check.

Mitigation: Recheck the official CoAnimator source before publication and base migration claims on same-day, same-input pilot results rather than comparative marketing language.

Risk: AI-HIVE tool calls, uploads, pricing checks, and generated-media tasks can create approval, budget, or asset-rights issues.

Mitigation: Review those actions before approval, use only owned or authorized assets, preserve source identifiers and file hashes, and keep the original CoAnimator path available for rollback.

## Reference(s):

- [CoAnimator official source](https://coanimator.com/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [CoAnimator official evidence and migration boundaries](references/platform-evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/coanimator-agent-ai-hive-migration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with structured checklists, tables, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration boundaries, pilot deliverables, agent handoff fields, AI-HIVE MCP work-order guidance, quality metrics, approval gates, and rollback criteria.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

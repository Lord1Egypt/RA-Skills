## Description:

AgentMem is a multi-agent memory and dispatch system with four-tier memory (HOT/WARM/COLD/ARCHIVE), cross-channel sharing, and a dispatch loop with auto-learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenshuangl](https://clawhub.ai/user/wenshuangl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building multi-agent systems use AgentMem to add local memory tiers, cross-channel recall, and dispatch feedback loops for choosing agents based on prior task outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived facts may be persisted locally and later retrieved across channels or agents.

Mitigation: Use non-sensitive data until retention, purge, and agent-scoping controls are reviewed and configured for the deployment.

Risk: Cross-agent sharing can expose memory to agents beyond the original context.

Mitigation: Review sharing rules, isolate private categories, and test agent ID enforcement before enabling multi-agent memory sharing.

Risk: Dispatch gateway behavior may send task content to a configured URL.

Mitigation: Allowlist trusted local or internal gateway URLs and disable auto-dispatch where URL routing is not required.

Risk: Background bridge launch behavior can start additional local processes.

Mitigation: Review bridge startup paths and run the skill with least-privilege local permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenshuangl/skills/agent-mem)
- [Publisher profile](https://clawhub.ai/user/wenshuangl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python module references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may refer to local memory files and ChromaDB-backed vector storage.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

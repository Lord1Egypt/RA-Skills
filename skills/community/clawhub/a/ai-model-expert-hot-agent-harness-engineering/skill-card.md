## Description:

This Chinese-language skill helps agent architects, platform engineers, and enterprise development teams design AI-HIVE agent harnesses with layered architecture, tool contracts, state models, evaluation gates, and runbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent architects, platform engineers, and enterprise R&D teams use this skill to turn AI-HIVE agent goals into maintainable harness designs. It guides model routing, tool contracts, memory and state design, evaluation gates, permissions, observability, and operational handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation can route ordinary API, workflow, or agent questions through this skill unexpectedly.

Mitigation: Disable implicit invocation or narrow the trigger terms before deployment in shared or production environments.

Risk: The helper script reads AI_HIVE_API_KEY and supports an AI_HIVE_BASE_URL override, which could expose credentials if pointed at an untrusted endpoint.

Mitigation: Keep the API key in a secure environment variable, use the official AI-HIVE endpoint, and set AI_HIVE_BASE_URL only for destinations that are fully trusted.

Risk: Model availability, pricing, and rankings can become stale.

Mitigation: Query current models and pricing snapshots at runtime, show candidate differences to the user, and avoid silent model substitution.

Risk: Paid, batch, external publishing, deletion, or privilege-changing actions can have irreversible or cost-bearing effects.

Mitigation: Require explicit human confirmation and keep task IDs, input hashes, statuses, outputs, and approval records before those actions proceed.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [Harness Agents official documentation](https://developer.harness.io/3k-docs/ai/harness-agents/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-hot-agent-harness-engineering)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON execution plans and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-routing rationale, pricing snapshot reminders, task ledger fields, approval gates, and validation checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

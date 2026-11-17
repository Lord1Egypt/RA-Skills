## Description:

Cognition provides a practical memory architecture for OpenClaw agents that need durable commitments, retrievable context, safer staged updates, reusable procedures, and memory hygiene across Core, Recommended, and Advanced adoption tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Cognition to add durable local memory practices to OpenClaw agents, including daily logs, compact durable knowledge, commitment tracking, staged consolidation, procedure capture, and retrieval hygiene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent future-intent behavior can execute broad deferred actions later without a clear approval gate.

Mitigation: Before enabling future intents, require explicit approval, narrow triggers, expiration, and audit logging for deferred actions.

Risk: Durable memory updates can preserve incorrect or stale information if proposals are accepted without review.

Mitigation: Use the skill's staged consolidation flow, keep raw logs append-only, preserve provenance, and require review for uncertain items.

## Reference(s):

- [Cognition - Architecture Notes](references/architecture.md)
- [Cognition - Protocol Blocks for AGENTS.md](references/protocols.md)
- [Nightly Consolidation - Safe Staging Prompt](references/consolidation-prompt.md)
- [Weekly Reflection - Analysis and Recommendations Only](references/weekly-reflection-prompt.md)
- [Cognition - Tier 2 Retrieval Configuration](references/config.md)
- [Cognitive Science Appendix](references/cognitive-science.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, prompt templates, and local memory file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can scaffold local memory directories and templates; scheduled workflows produce staged Markdown reports and recommendations.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

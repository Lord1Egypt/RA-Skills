## Description:

Persistent SQLite memory for Hermes and OpenClaw that stores facts, snippets, lessons, entities, relations, and provenance with authority lanes, conflict controls, and bounded plugin recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmannixx](https://clawhub.ai/user/xmannixx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Agent Memory to add persistent, auditable memory to Hermes or OpenClaw agents. It is intended for cross-session recall with separated authority lanes for identity, preferences, evidence, authorization, procedural rules, snippets, and lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may retain privacy-sensitive or secret data across sessions and recall it into future prompts.

Mitigation: Review what the memory plugin stores before installation, avoid storing secrets or sensitive personal data, and maintain procedures to inspect, disable, and delete stored memories.

Risk: The release security guidance calls out missing implementation files and a cleanup timer unit as items that must be trusted before installation.

Mitigation: Confirm those files and the timer unit come from the trusted publisher source before enabling the plugin or scheduled cleanup.

Risk: Automatic memory injection can influence agent behavior through retained context.

Mitigation: Use the documented authority lanes, source restrictions, procedural-rule human review gate, and bounded recall budgets; audit recalled memory regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmannixx/skills/agent-memory-2)
- [Server-resolved GitHub provenance](https://github.com/xMannixx/agent-memory-skill/tree/main/memory/agent-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes persistent SQLite memory, CLI usage, plugin installation, bounded recall, audit/provenance commands, and cleanup behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

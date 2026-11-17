## Description:

基于双环架构的AGI进化模型，通过意向性分析、人格层映射和元认知检测实现持续自我演进；当用户需要智能对话、人格定制或复杂问题求解时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate an AGI-style digital companion for intelligent dialogue, personality customization, and complex problem solving. It guides an agent through local Python tools for memory, intent analysis, personality mapping, metacognition, and self-correction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic personality setup and local memory creation can persist user or personality data without clear opt-in.

Mitigation: Require explicit user consent before creating ./agi_memory or storing interaction data, and provide clear retention and deletion controls.

Risk: The calculator path is reported as able to execute arbitrary Python code.

Mitigation: Replace eval-style execution with a restricted math parser and allow only approved operators and functions.

Risk: Raw user content may be stored or logged during memory, history, and advice-pool workflows.

Mitigation: Minimize stored content, redact sensitive data, and store raw user content only after explicit user agreement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiwifruit13/skills/agi-evolution-model-basic)
- [Architecture](references/architecture.md)
- [Capability Boundaries](references/capability_boundaries.md)
- [Intentionality Architecture](references/intentionality_architecture.md)
- [Metacognition Check Component](references/metacognition-check-component.md)
- [Cognitive Insight V2 Implementation](references/cognitive-insight-v2-implementation.md)
- [Personality Mapping](references/personality_mapping.md)
- [Tool Use Specification](references/tool_use_spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code paths, and JSON configuration or state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local ./agi_memory files for personality, history, memory, and analysis state when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Provides Chinese-language AI agent architecture patterns for designing or refactoring tool systems, safety gates, context compression, and task orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi488](https://clawhub.ai/user/wudi488)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent framework engineers use this skill as a reference template pack when designing permission gates, lazy tool loading, context compression, and read/write scheduling for agent harnesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety-critical templates may lead to unsafe authorization behavior if copied directly into a production agent.

Mitigation: Review and adapt generated permission-gate code, including authorization state and approval binding, before use.

Risk: Context compression templates may remove or weaken important safety messages if implemented without safeguards.

Mitigation: Preserve all system and developer safety messages when adapting context-compression logic.

Risk: Template code may not match a target project's security, concurrency, or deployment requirements.

Mitigation: Test adapted code in a branch or sandbox and avoid overwriting existing files without explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wudi488/skills/claude-code-architecture)
- [SKILL.md](SKILL.md)
- [Permission gate implementation](references/permission_gate_full.py)
- [Tool lazy loading implementation](references/tool_lazy_loading_full.py)
- [Context compressor implementation](references/context_compressor_full.py)
- [Read/write scheduler implementation](references/rw_scheduler_full.py)
- [Framework comparison](references/framework_comparison.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code examples and reference implementations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language architecture guidance; generated code should be reviewed and adapted before use.]

## Skill Version(s):

2.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

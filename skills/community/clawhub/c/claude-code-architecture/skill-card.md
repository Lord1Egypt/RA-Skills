## Description: <br>
Claude Code Architecture provides AI agent architecture patterns for tool systems, safety gates, context compression, and task orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi488](https://clawhub.ai/user/wudi488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design or refactor AI agent harness architecture, including permission gates, lazy tool loading, context compression, and read/write task scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated architecture templates could be written into a real project without sufficient review. <br>
Mitigation: Confirm the destination path, review the diff, and test changes in a branch or sandbox before deployment. <br>
Risk: Reference implementations may need adaptation for a project's actual permissions, tools, and context limits. <br>
Mitigation: Treat the bundled implementations as design references and adjust them to the target system before use. <br>
Risk: Incorrect permission or scheduling configuration could allow actions that should require approval. <br>
Mitigation: Use fail-closed defaults, require explicit approval for write actions, and audit generated permission changes. <br>


## Reference(s): <br>
- [Permission Gate Full Implementation](references/permission_gate_full.py) <br>
- [Tool Lazy Loading Full Implementation](references/tool_lazy_loading_full.py) <br>
- [Context Compressor Full Implementation](references/context_compressor_full.py) <br>
- [Read/Write Scheduler Full Implementation](references/rw_scheduler_full.py) <br>
- [Agent Framework Architecture Comparison](references/framework_comparison.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with Python code templates and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated templates should be reviewed and adapted before use in a project.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

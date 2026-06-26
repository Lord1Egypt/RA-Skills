## Description: <br>
Use when creating, editing, debugging, or validating Dify workflow DSL for self-hosted Dify. Start from an exported workflow of the target instance, edit minimally, and verify by re-importing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arn0ld87](https://clawhub.ai/user/arn0ld87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, edit, debug, and validate Dify workflow DSL for self-hosted Dify instances. It emphasizes export-first, minimal workflow changes, local YAML validation, and re-import checks on the same target instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example templates may include HTTP or LLM nodes that call external services if adapted and run in Dify. <br>
Mitigation: Inspect every HTTP and LLM node before use, replace example endpoints and providers deliberately, and avoid sending sensitive or regulated data to external providers without approval. <br>
Risk: Workflow edits can break imports or overwrite working self-hosted Dify workflows when applied without matching the target instance export. <br>
Mitigation: Start from an exported workflow from the target instance, keep changes minimal, run local YAML validation, and keep an exported backup before re-importing changes. <br>
Risk: Secrets may be exposed if API keys are embedded directly in workflow YAML, prompts, or code nodes. <br>
Mitigation: Keep secrets in Dify environment variables or instance configuration and review workflow content before importing. <br>


## Reference(s): <br>
- [Dify Documentation](https://docs.dify.ai/) <br>
- [Dify GitHub Repository](https://github.com/langgenius/dify) <br>
- [Dify Releases](https://github.com/langgenius/dify/releases) <br>
- [Dify Workflow DSL Structure](references/workflow_structure.md) <br>
- [Dify Workflow Node Types Reference](references/node_types.md) <br>
- [Dify Workflow Edge Types and Connections](references/edge_types.md) <br>
- [Dify Variable Syntax Complete Guide](references/variable-syntax.md) <br>
- [Dify Workflow Common Gotchas](references/common-gotchas.md) <br>
- [Dify Node Templates Reference](references/node-templates.md) <br>
- [Current Workflow Patterns](references/current_patterns.md) <br>
- [Advanced Workflow Patterns](references/advanced_patterns.md) <br>
- [Workflow Retrieval Patterns](references/retrieval_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Dify workflow DSL edits, validation steps, node IDs, and import or rollback checklists.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

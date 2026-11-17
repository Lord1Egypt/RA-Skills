## Description:

Orchestrates long, structured multi-chapter document generation with sub-agents by using dependency analysis, contract-first decomposition, serial and parallel scheduling, file isolation, state persistence, and consistency validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolayao](https://clawhub.ai/user/nicolayao)

### License/Terms of Use:


## Use Case:

Developers and writers use this skill to plan and generate long structured documents that need shared definitions, cross-section consistency, sub-agent file isolation, persisted orchestration state, and final merge validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to create and update task-specific Markdown and JSON files, which can clutter a workspace or collide with existing filenames.

Mitigation: Run the skill in a dedicated project or task directory and review planned filenames before allowing writes.

Risk: Sub-agent outputs can repeat document titles, write the wrong chapter content, or diverge from shared definitions.

Mitigation: Use the contract-first workflow, isolated chapter files, duplicate-title stripping, and final consistency checks before delivery.

Risk: Sensitive document sections may trigger sub-agent content filters.

Mitigation: Retry with safer phrasing or have the main agent write the blocked section directly, as described in the artifact guidance.

## Reference(s):

- [Doc Orchestrator on ClawHub](https://clawhub.ai/nicolayao/skills/doc-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON state examples, shell command snippets, and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task-scoped contract, chapter, orchestration state, and final document files when applied by an agent.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

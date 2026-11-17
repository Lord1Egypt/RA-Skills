## Description:

Build and maintain a structured PDE equation registry, analyze competition tasks including difficulty, bottlenecks, and score projections, generate strategic recommendations for research focus, and expose this intelligence via CLI and MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research engineers use this skill to inspect PDE competition tasks, compare equation-level metadata and scoring constraints, and plan which experiments or submissions to prioritize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned tool execution can run an unexpected package version.

Mitigation: Use pinned package versions when launching or installing the related CLI tools.

Risk: MCP tools can expand what an agent is allowed to call.

Mitigation: Review MCP tool definitions and only add trusted servers to the agent configuration.

Risk: Experiment credentials or dataset paths could be exposed if stored in tracked files.

Mitigation: Keep ClearML, Langfuse, and dataset credentials in local untracked environment or config files.

## Reference(s):

- [Expflow project homepage](https://github.com/diamond2nv/expflow)
- [Competition Task Intelligence on ClawHub](https://clawhub.ai/diamond2nv/skills/competition-task-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local configuration files and MCP setup for agent integration.]

## Skill Version(s):

0.7.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

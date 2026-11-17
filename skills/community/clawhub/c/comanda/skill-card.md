## Description:

Comanda helps agents generate, visualize, edit, and run declarative YAML AI pipelines with the comanda CLI across multiple model providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kris-hansen](https://clawhub.ai/user/kris-hansen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, inspect, refine, and run Comanda workflow YAML for LLM pipelines, including file-based data flow, parallel fan-in, branching, tool steps, and agentic loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows can include shell tool steps, URL inputs, codebase indexing, or agentic loops that may act on local files or external content.

Mitigation: Review generated workflow YAML before execution, keep command allowlists and allowed paths narrow, and run tool-enabled workflows only when the workflow source is trusted.

## Reference(s):

- [Comanda homepage](https://comanda.sh)
- [Comanda Workflow Spec](references/WORKFLOW-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow YAML, CLI commands, configuration guidance, and review notes for generated Comanda workflows.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

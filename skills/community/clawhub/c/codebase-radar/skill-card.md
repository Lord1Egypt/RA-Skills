## Description:

Scan codebase for dependency graph, tech debt hotspots, and module health scores

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a codebase for dependency structure, module health, tech debt signals, dead code, and refactoring priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is read-only, but weak path and limit controls may read or report files outside the intended project.

Mitigation: Run it only on trusted repositories or inside a constrained workspace, check for symlinks and very large trees first, and do not rely on --exclude or --max-files as complete read boundaries.

Risk: Generated Mermaid output from untrusted code may carry untrusted text into downstream documentation or renderers.

Mitigation: Review generated diagrams before publishing or rendering them in privileged contexts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance]

**Output Format:** [Plain text, JSON, Markdown reports, and Mermaid dependency diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project summaries, dependency edges, circular dependency counts, tech debt findings, health scores, and ranked refactoring priorities.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Fusion Workflow Hub helps agents combine Graphify code knowledge graphs, ECC workflows, and OpenClaw automation for codebase analysis, TDD-oriented development, review, and continuous learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuang-he](https://clawhub.ai/user/zhuang-he)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand codebase structure, run standardized planning and review workflows, and use Graphify-backed analysis during complex programming tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on third-party Python package installation.

Mitigation: Install in an isolated environment such as virtualenv, pipx, or uv, and review or pin dependency versions where possible.

Risk: Graph building can create local artifacts from the analyzed project and documents.

Mitigation: Run graph building only on intended directories and avoid including secrets or private documents unless local graph artifacts are acceptable.

## Reference(s):

- [Graphify command reference](references/graphify-commands.md)
- [Everything Claude Code best practices](references/ecc-best-practices.md)
- [Graphify](https://github.com/safishamsi/graphify)
- [Everything Claude Code](https://github.com/probinger/00-everything-claude-code)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown with inline shell commands and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Graphify outputs such as graph.html, GRAPH_REPORT.md, graph.json, and cache files when the agent runs the referenced commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

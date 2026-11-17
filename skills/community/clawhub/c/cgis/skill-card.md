## Description:

Use when a question is about how code connects rather than what a single file says: finding callers, assessing renames or signature changes, tracing execution paths, mapping modules, and checking architectural drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaebee](https://clawhub.ai/user/zaebee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use CGIS to answer structural codebase questions with a project-local graph, including impact analysis, flow tracing, symbol lookup, module mapping, metrics, drift checks, and reachability audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing too broad a path can include secrets, dependencies, virtual environments, or unrelated private material in the local graph.

Mitigation: Point ingestion at the intended source directory, such as ./src, and avoid whole-repository ingestion when the repository contains unrelated or sensitive material.

Risk: A stale or incomplete static graph can produce confident but wrong structural answers.

Mitigation: Re-run cgis_ingest after substantial changes, check cgis_validate when unresolved edges are high, and treat empty impact results as no static callers found rather than proof that deletion is safe.

Risk: The graph does not cover languages outside Python and TypeScript.

Mitigation: Fall back to direct file inspection for unsupported languages and state which parts of the answer were outside graph coverage.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zaebee/codegraph-brain/tree/main/plugin/skills/cgis)
- [Guardian graph-aware code review README section](https://github.com/zaebee/codegraph-brain#-guardian-graph-aware-code-review)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code analysis, Configuration]

**Output Format:** [Markdown with inline tool calls and shell-style commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a project-local graph database and covers Python and TypeScript source files.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

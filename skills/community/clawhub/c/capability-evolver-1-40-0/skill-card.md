## Description:

A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengyu199009](https://clawhub.ai/user/zengyu199009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze agent runtime history, generate protocol-constrained evolution guidance, manage reusable GEP assets, and run reviewable repair or improvement cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spawn code-changing agent workflows, ingest remote instructions, and alter installed agent behavior.

Mitigation: Install only in a sandboxed workspace with clean git state, use review mode by default, and disable bridge, loop, auto-publish, auto-issue, and auto-update behavior unless explicitly needed.

Risk: The skill can send local context to external services and uses authenticated EvoMap, GitHub, and optional memory graph endpoints.

Mitigation: Use no production secrets, limit network access to trusted origins, and do not point A2A_HUB_URL or MEMORY_GRAPH_REMOTE_URL at untrusted endpoints.

Risk: Validation or dependency-healing behavior may execute shell commands such as git, node, npm, process inspection, and disk checks.

Mitigation: Keep execution permissions narrowly scoped, avoid generic npm or npx validation from remote Genes, and review command-producing output before running it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zengyu199009/skills/capability-evolver-1-40-0)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zengyu199009)
- [EvoMap Hub](https://evomap.ai)
- [EvoMap GEP Documentation](https://evomap.ai/wiki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text guidance with inline shell commands and JSON-backed evolution assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local GEP asset and memory files; host runtimes may interpret emitted directives.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package version 1.40.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Agent Dev Toolkit helps developers build, automate, document, and monetize AI agents using bundled agent-building, browser automation, wallet, development, and documentation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobem0706](https://clawhub.ai/user/tobem0706)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this toolkit to create OpenClaw agents, define operating rules and documentation, automate browser workflows, and optionally integrate wallet workflows with explicit controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet component can document high-impact transfers, swaps, and arbitrary EVM transactions.

Mitigation: Do not use real funds until spending policies are configured, transaction approvals are required, API keys are protected, and arbitrary calldata is disabled or tightly allowlisted.

Risk: Broad agent permissions can expose files, writes, shell commands, or web access beyond the current task.

Mitigation: Restrict file access, write access, Bash commands, and WebFetch domains to the specific project and task before installing or using the toolkit.

Risk: Unpinned or unreviewed installations can introduce supply-chain uncertainty.

Mitigation: Prefer pinned versions or reviewed commits for installation.

## Reference(s):

- [Agent Dev Toolkit on ClawHub](https://clawhub.ai/tobem0706/skills/agent-dev-toolkit)
- [README](README.md)
- [Installation Guide](INSTALL.md)
- [Agent Browser Overview](dependencies/agent-browser-core/references/agent-browser-overview.md)
- [Safety and Risk Controls](dependencies/agent-browser-core/references/agent-browser-safety.md)
- [Agent Browser Workflows](dependencies/agent-browser-core/references/agent-browser-workflows.md)
- [OpenClaw Agent Workspace](dependencies/agent-builder/references/openclaw-workspace.md)
- [OpenClaw Agent File Templates](dependencies/agent-builder/references/templates.md)
- [Agent Architecture Patterns](dependencies/agent-builder/references/architecture.md)
- [Agent Docs Advanced Patterns](dependencies/agent-docs/references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, configuration snippets, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and the OpenClaw/ClawHub CLI environment described by the artifact metadata.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

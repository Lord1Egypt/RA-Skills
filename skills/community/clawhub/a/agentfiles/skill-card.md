## Description:

Use this skill when you need to publish, fetch, search, list, share, or watch AgentFiles artifacts from Codex, Claude Code, OpenClaw, or other agent runtimes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hammadtq](https://clawhub.ai/user/hammadtq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentFiles to move artifacts and handoff context across Codex, Claude Code, OpenClaw, and other supported runtimes. The skill helps agents choose the existing AgentFiles CLI or MCP handoff path for publishing, fetching, sharing, searching, listing, and watching artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AgentFiles publish, share, and handoff commands can transmit conversation context or artifact content to another namespace, recipient, or share URL.

Mitigation: Review the recipient, namespace, payload, and share destination before approving publish, share, or handoff actions.

Risk: The fallback path can download mutable npm code at runtime.

Mitigation: Prefer a pinned or administrator-installed AgentFiles CLI and review package provenance before first use.

Risk: Watcher automation can execute local scripts for emitted events.

Mitigation: Use watch --exec only with trusted executable paths and inspect automation scripts before enabling them.

Risk: Share URLs and API keys can expose access if copied into logs, prompts, or command history.

Mitigation: Treat share URLs and credentials as secrets, and avoid command-line API keys unless a user explicitly chooses the manual configuration path.

## Reference(s):

- [AgentFiles homepage](https://agentfiles.io)
- [ClawHub skill page](https://clawhub.ai/hammadtq/skills/agentfiles)
- [AgentFiles command matrix](references/commands.md)
- [AgentFiles runtime notes](references/runtime-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local AgentFiles CLI configuration and browser-approved authentication flows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

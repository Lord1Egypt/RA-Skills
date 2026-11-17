## Description:

Complete toolkit for building AI agents, including agent-builder, agent-browser, agent-wallet, agent-development, and agent-docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cahdieng](https://clawhub.ai/user/cahdieng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this toolkit to create and tune OpenClaw or Claude Code agents, automate browser workflows, configure agent wallets, and write agent-oriented documentation. The skill is aimed at external users building reusable agent workspaces and operational playbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote wallet controls can move funds before safeguards are configured.

Mitigation: Use empty or testnet wallets until the owner has claimed the wallet and configured strict spending, address, token, function, and approval policies.

Risk: Generated agents may receive overly broad Write, Edit, Bash, or web access.

Mitigation: Use narrow per-agent tool and domain allowlists, and avoid granting blanket unattended permissions.

Risk: Wallet bearer tokens, API keys, or platform credentials may be exposed through prompts, files, shell history, or logs.

Mitigation: Keep secrets out of prompts and generated files, redact logs, and store credentials only in approved secret-management channels.

## Reference(s):

- [README](README.md)
- [Installation Guide](INSTALL.md)
- [Agent Browser Overview](dependencies/agent-browser-core/references/agent-browser-overview.md)
- [Agent Browser Command Map](dependencies/agent-browser-core/references/agent-browser-command-map.md)
- [Agent Browser Safety](dependencies/agent-browser-core/references/agent-browser-safety.md)
- [Agent Browser Workflows](dependencies/agent-browser-core/references/agent-browser-workflows.md)
- [Agent Builder Workspace](dependencies/agent-builder/references/openclaw-workspace.md)
- [Agent Builder Templates](dependencies/agent-builder/references/templates.md)
- [Agent Docs Advanced Patterns](dependencies/agent-docs/references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands, JSON snippets, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and ClawHub/OpenClaw CLI workflows; wallet operations require bearer tokens and configured policy controls.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

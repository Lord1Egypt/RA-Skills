## Description:

Self-orchestrating multi-agent development workflows. You say WHAT, the AI decides HOW.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongbai233](https://clawhub.ai/user/kongbai233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multi-agent software development workflows for features, bug fixes, API changes, research, refactoring, and releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents through broad file, shell, GitHub, and release workflows.

Mitigation: Use it first in a sandbox or protected branch and require explicit approval before local writes, pull requests, merges, tags, releases, CI/CD actions, or credentialed GitHub operations.

Risk: Full workflow usage may require network access, local binaries, credentials, and MCP packages.

Mitigation: Review and pin MCP packages before use, provide only the credentials required for the current task, and confirm installed binaries before starting a workflow.

Risk: The security verdict is suspicious because approval gates are not consistently defined for autonomous runtime actions.

Mitigation: Keep human review gates around code changes, shell commands, repository operations, and generated release artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongbai233/skills/cc-godmode-5-11-3)
- [OpenClaw GodMode repository](https://github.com/cubetribe/openclaw-godmode-skill)
- [Original GodMode repository](https://github.com/cubetribe/ClawdBot-GodMode)
- [OpenClaw](https://openclaw.ai)
- [Claude Code](https://claude.ai/code)
- [Workflow documentation](docs/WORKFLOWS.md)
- [Agent specifications](docs/AGENTS.md)
- [Migration guide](docs/MIGRATION.md)
- [Troubleshooting guide](docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, workflow reports, and code or configuration changes when invoked by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only package; runtime outputs depend on the agent tools and workflow selected by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); packaged skill metadata reports 5.11.3

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

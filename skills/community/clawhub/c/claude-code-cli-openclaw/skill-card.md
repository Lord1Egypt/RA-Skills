## Description:

Install, authenticate, and use Claude Code CLI as a native coding tool for any OpenClaw agent system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to install Claude Code CLI, authenticate it with a Claude Max OAuth token, and configure it as a coding tool for file-aware implementation, refactoring, bug fixing, scaffolding, and review tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses persistent storage of a long-lived Claude Code OAuth token.

Mitigation: Use a secret store when available, avoid storing the token in /etc/environment or shell startup files for shared systems, never print or commit the full token, and rotate or revoke it if exposure is suspected.

Risk: The installer uses an unpinned global npm package install for @anthropic-ai/claude-code.

Mitigation: Review the package source and lock to an approved version before broad deployment; avoid running the installer as root.

Risk: Claude Code CLI can read and modify project files when used as a coding tool.

Mitigation: Run it in a controlled workspace, review proposed file changes, and use version control branches plus build or test checks before merging.

Risk: OpenClaw backend and fallback configuration can route coding tasks through the external CLI.

Mitigation: Review the OpenClaw configuration patch before enabling it broadly and restrict where the CLI backend is available.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/asif2bd/skills/claude-code-cli-openclaw)
- [ProSkills Listing](https://proskills.md/skills/claude-code-cli)
- [GitHub Repository](https://github.com/ProSkillsMD/skill-claude-code-cli)
- [MissionDeck.ai](https://missiondeck.ai)
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code CLI on npm](https://www.npmjs.com/package/@anthropic-ai/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, OAuth setup, OpenClaw configuration, workflow, troubleshooting, and security guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

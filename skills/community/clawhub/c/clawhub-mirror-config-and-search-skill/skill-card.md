## Description:

Configures the ClawHub domestic mirror to reduce rate-limit and timeout issues, install Multi Search Engine, guide multi-engine search strategies, and archive the configuration workflow for reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger0808](https://clawhub.ai/user/roger0808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when ClawHub skill installation is slow, rate-limited, or timing out. It provides mirror configuration commands, Multi Search Engine installation guidance, search-engine selection tips, and knowledge-base archiving steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route ClawHub traffic through cn.clawhub-mirror.com when the user did not explicitly request that registry.

Mitigation: Require explicit user confirmation before changing registry settings or running install/update commands against the mirror.

Risk: The skill encourages broad package updates and persistent environment-variable changes.

Mitigation: Prefer one-command registry flags, pinned and verified packages, and narrowly scoped installs before making persistent configuration changes.

Risk: The skill may propose edits across knowledge-base files, multiple workspaces, and Git history.

Mitigation: Review all file changes before applying them, and require confirmation before cross-workspace sync, Git commit, or Git push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roger0808/skills/clawhub-mirror-config-and-search-skill)
- [ClawHub mirror registry](https://cn.clawhub-mirror.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose registry changes, environment-variable persistence, knowledge-base edits, cross-workspace sync, and Git operations that require user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

CocoLoop helps agents search, download, install, update, uninstall, and safety-check skills across supported agent platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catrefuse](https://clawhub.ai/user/catrefuse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use CocoLoop to locate, evaluate, install, update, uninstall, and safety-check skills for Codex, Claude Code, OpenClaw, OpenCode, and related agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can download remote skill packages and write them into directories loaded by agent platforms.

Mitigation: Install only from trusted or reviewed sources, inspect the selected skill before installation, and run the provided safety-check workflow for unfamiliar sources.

Risk: Forced install or uninstall paths can overwrite or delete local skill directories.

Mitigation: Check resolved destination paths before using force options, keep backups for important local skills, and confirm the target when multiple installations exist.

Risk: SafeScan operations may upload local files or paths to the configured scanning service.

Mitigation: Do not scan sensitive files unless upload is intended, and review the selected scan target before submitting it.

## Reference(s):

- [CocoLoop ClawHub listing](https://clawhub.ai/catrefuse/skills/cocoloop)
- [README](README.md)
- [Installation guide](references/install-guide.md)
- [Search guide](references/search-guide.md)
- [Operations manual](references/operations-manual.md)
- [Uninstall guide](references/uninstall-guide.md)
- [Safety check guide](references/safety-check-guide.md)
- [CocoLoop Safe Check standard](references/cocoloop-safe-check.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell commands, paths, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to call bundled shell wrappers for search, inspect, install, update, uninstall, featured recommendations, health checks, and SafeScan operations.]

## Skill Version(s):

0.5.0 (source: ClawHub release evidence; artifact frontmatter reports 0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

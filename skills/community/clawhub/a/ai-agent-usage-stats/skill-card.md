## Description:

Token Stats reads local AI assistant usage files so users can choose an agent and view token, cache, call-count, comparison, monitoring, and export statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyiling1111](https://clawhub.ai/user/huyiling1111)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users use Token Stats to inspect local token consumption, monitor live usage, compare time periods, and export usage records across supported coding assistants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local assistant logs and databases that may contain sensitive usage metadata.

Mitigation: Run it only on machines where local assistant usage data is approved for inspection, and review file access expectations before installation.

Risk: Setup makes persistent PATH and wrapper-command changes.

Mitigation: Review the setup changes before use and use the provided uninstall path or manual shell profile cleanup if the command should be removed.

Risk: The built-in update path can replace files from a mismatched package name.

Mitigation: Avoid the built-in agent-usage-stats update/--update path until fixed; use the canonical ClawHub package update and verify installed files.

Risk: On Windows/WSL, saved paths in ~/.config/agent-usage-stats/paths.json influence WSL execution.

Mitigation: Review the saved paths configuration on Windows/WSL systems before relying on collected results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huyiling1111/skills/ai-agent-usage-stats)
- [README.en.md](README.en.md)
- [Model Price Configuration](model_prices.toml)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Terminal text tables with optional XLSX, CSV, or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local assistant usage data and model price configuration; no network access is needed for statistics collection.]

## Skill Version(s):

2.6.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

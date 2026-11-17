## Description:

Dep Radar scans project dependencies for outdated packages, breaking changes, affected code locations, migration notes, and community pain signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarun-khatri](https://clawhub.ai/user/tarun-khatri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and CI operators use this skill to assess dependency upgrade risk before changing package versions. It identifies likely breaking changes, ranks upgrade risk, and points to impacted files and relevant migration reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic SessionStart hook can execute shell code from a project configuration file.

Mitigation: Disable or fix the hook so dotenv files are parsed as data rather than sourced as shell.

Risk: Project-controlled .claude/depradar.env files can influence behavior in untrusted repositories.

Mitigation: Avoid project-level configuration in untrusted repositories and prefer reviewed user-level configuration.

Risk: Optional npm dependency installation during setup can introduce unreviewed package changes.

Mitigation: Pin or skip automatic npm installation unless the dependency and version are reviewed.

Risk: Registry, community-search, and notification integrations may use API tokens or webhook URLs.

Mitigation: Use least-privilege tokens and send notifications only to webhook URLs you control.

## Reference(s):

- [ClawHub Dep Radar Skill Page](https://clawhub.ai/tarun-khatri/skills/depradar)
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown reports, JSON reports, and concise agent guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include package versions, scores, affected file paths, migration notes, community-signal summaries, and optional notification output.]

## Skill Version(s):

2.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

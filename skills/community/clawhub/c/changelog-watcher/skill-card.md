## Description:

Monitors GitHub repositories and npm packages for new releases and version updates, summarizes changelogs, and highlights likely breaking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to monitor configured GitHub repositories and npm packages, detect new releases, and generate concise markdown changelog reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured repository and package names are sent to GitHub and npm during checks.

Mitigation: Use watchlists that disclose only repositories and packages you are comfortable querying through those services.

Risk: Using --update-state advances local state and can affect which releases appear in later reports.

Mitigation: Use the dry-run command when reviewing results without changing state.json.

Risk: Fetched release notes are untrusted external content.

Mitigation: Review release notes before acting on upgrade guidance or commands.

Risk: Scheduled checks create repeated external network calls and local persistence.

Mitigation: Schedule checks only when intended, and choose a cadence that fits API rate limits and monitoring needs.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/changelog-watcher)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional JSON release data and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local state.json when --update-state is used; dry-run leaves state unchanged.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

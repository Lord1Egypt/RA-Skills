## Description:

AI competitive intelligence pipeline for analyzing competitors, generating reports, and tracking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalianmao000](https://clawhub.ai/user/dalianmao000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and strategy teams use this skill in Claude Code to maintain competitor trackers, research companies and pricing, compare vendors, and generate competitive intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and export workflows can install or execute npm and Python dependencies and change local project files.

Mitigation: Install in a dedicated project or container, review setup commands before running them, and pin npm and Python dependencies.

Risk: Monitor mode can create persistent scheduled automation.

Mitigation: Require explicit approval before enabling monitor mode and review the schedule before use.

Risk: Company names can flow into filesystem paths or shell commands.

Mitigation: Sanitize company names before any filesystem or shell operation.

Risk: The workflow may run with API keys or other secrets in the environment.

Mitigation: Avoid running setup or monitoring with unnecessary secrets present, and scope credentials such as TAVILY_API_KEY to the project only when needed.

## Reference(s):

- [Project homepage](https://github.com/dalianmao000/competitive-ops-v2)
- [ClawHub listing](https://clawhub.ai/dalianmao000/skills/competitive-ops)
- [README](README.md)
- [Setup Guide](docs/SETUP.md)
- [Customization Guide](docs/CUSTOMIZATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, optional HTML/PDF/PNG exports, JSON snapshots, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local tracker, report, snapshot, and export files when the user invokes those modes.]

## Skill Version(s):

1.0.0 (source: server release metadata and marketplace.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

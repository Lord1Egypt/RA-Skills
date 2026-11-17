## Description:

Common-Fetcher is a data collection framework for AI agents that supports RSS, web, and API sources with AI scoring, classification, and summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lq707904686](https://clawhub.ai/user/lq707904686)

### License/Terms of Use:

MIT License

## Use Case:

Developers and AI-agent builders use Common-Fetcher to collect industry and AI-technology information from preconfigured or custom RSS, web, and API sources, then generate Markdown or JSON outputs for review or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs a mutable npm command-line package whose reviewed source and exact package version are not included in the artifact.

Mitigation: Use a pinned and reviewed npm package version before installation, especially in sensitive environments.

Risk: Automated collection can access broad external RSS, web, and API sources and write reports to configured output locations.

Mitigation: Run with limited filesystem and environment access, and configure allowed sources, schedules, output locations, and retention before enabling automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lq707904686/skills/common-fetcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Configuration]

**Output Format:** [Markdown, JSON, command-line examples, TypeScript API examples, and OpenClaw configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on configured sources, schedules, article limits, timeouts, and destination paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
